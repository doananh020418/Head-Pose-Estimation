import cv2
import time
import FaceLandmarkModule as F
import numpy as np
# Nose tip					id:1
# Chin						id:175
# Left eye left corner		id:247
# Right eye right corner	id:467
# Left Mouth corner			id:57
# Right mouth corner		id:287
def estimatePose(im,image_points):
	# face coordinate in real world
	noseTip =(0.0,0.0,0.0)
	Chin = (0.0, -330.0, -65.0)
	leftEyeLeftCorner = (-225.0, 170.0, -135.0)
	rightEyeRightCorner = (225.0, 170.0, -135.0)
	leftMouthCorner = (-150.0, -150.0, -125.0)
	rightMouthCorner = (150.0, -150.0, -125.0)

	model_points = np.array([
		(0.0,0.0,0.0),
		(0.0, -330.0, -65.0),
		(-225.0, 170.0, -135.0),
		(225.0, 170.0, -135.0),
		(-150.0, -150.0, -125.0),
		(150.0, -150.0, -125.0)
	])
	size = (1280,1080)
	focal_length = size[1]
	center = (size[1]/2,size[0]/2)
	camera_matrix = np.array([
		[focal_length,0,center[0]],
		[0,focal_length, center[1]],
		[0,0,1]],
		dtype = 'double'
	)

	dist_coeffs = np.zeros((4,1))
	(success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
																  dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
	for p in image_points:
		cv2.circle(im, (int(p[0]), int(p[1])), 3, (0,0,255), -1)

	(left_eye_end_point2D, jacobian) = cv2.projectPoints(np.array([(-225.0, 170.0, 1000.0)]), rotation_vector,
														 translation_vector, camera_matrix, dist_coeffs)
	p1 = (int(image_points[2][0]), int(image_points[2][1]))
	p2 = (int(left_eye_end_point2D[0][0][0]), int(left_eye_end_point2D[0][0][1]))
	cv2.line(im, p1, p2, (255, 0, 0), 2)

	(right_eye_end_point2D, jacobian) = cv2.projectPoints(np.array([(225.0, 170.0, 1000.0)]), rotation_vector,
														 translation_vector, camera_matrix, dist_coeffs)
	p3 = (int(image_points[3][0]), int(image_points[3][1]))
	p4 = (int(right_eye_end_point2D[0][0][0]), int(right_eye_end_point2D[0][0][1]))
	cv2.line(im, p3, p4, (255, 0, 0), 2)

	(chin_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, -330.0, 1000.0)]), rotation_vector,
														 translation_vector, camera_matrix, dist_coeffs)
	p5 = (int(image_points[1][0]), int(image_points[1][1]))
	p6 = (int(chin_end_point2D[0][0][0]), int(chin_end_point2D[0][0][1]))
	cv2.line(im, p5, p6, (255, 0, 0), 2)


	return im


def main():
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
	ptime = 0
	detector = F.FaceMeshDetector(maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)
	while True:
		if cap.isOpened():
			succ, img = cap.read()
			if succ:
				img = cv2.flip(img,1)

				img,faces = detector.findFaceMesh(img)
				if len(faces)!=0:
					#print(faces[175])
					image_points = np.array([
						faces[1],
						faces[175],
						faces[247],
						faces[467],
						faces[57],
						faces[287]
					],dtype="double")
					img = estimatePose(img,image_points)

				ctime = time.time()
				fps = 1/(ctime - ptime)
				ptime = ctime
				cv2.putText(img,f'FPS: {str(int(fps))}',(10,50),cv2.FONT_HERSHEY_SIMPLEX
							,1,(0,0,255),1)
				cv2.imshow("camera",img)
				cv2.waitKey(1)
	return

if __name__ == '__main__':
    main()
