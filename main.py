import cv2

import FaceLandmarkModule as F


def main():
    cap = cv2.VideoCapture(0)
    FaceDetector = F.FaceMeshDetector(maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)

    if cap.isOpened():
        while True:
            succ, img = cap.read()
            if succ:
                img = cv2.flip(img, 1)
                img, faceLandmark = FaceDetector.findFaceMesh(img)
                if len(faceLandmark) != 0:
                    for id,flm in enumerate(faceLandmark):
                        print(id,flm[0])

                cv2.imshow('camera', img)
                cv2.waitKey(1)
            else:
                return
    else:
        return


if __name__ == '__main__':
    main()
