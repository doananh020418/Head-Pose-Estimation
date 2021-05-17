import mediapipe as mp
import cv2

class FaceMeshDetector:
    def __init__(self, staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDetectionCon = minDetectionCon
        self.minTrackCon = minTrackCon

        self.faceMesh = mp.solutions.face_mesh.FaceMesh(self.staticMode, self.maxFaces, self.minDetectionCon,
                                                        self.minTrackCon)
        self.drawSpec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw=True):
        faces = []
        h,w,_ = img.shape
        self.RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.RGBimg)
        if self.results.multi_face_landmarks:
            for flm in self.results.multi_face_landmarks:
                if draw:
                    mp.solutions.drawing_utils.draw_landmarks(img, flm, mp.solutions.face_mesh.FACE_CONNECTIONS,
                                                             self.drawSpec, self.drawSpec)
                face = []
                for id,lm in enumerate(flm.landmark):
                    x,y = int(lm.x*h),int(lm.y*w)
                    face.append((x,y))
                #faces.append(face)
        return img,face