# Head-Pose-Estimation
What is pose estimation ?

In computer vision the pose of an object refers to its relative orientation and position with respect to a camera. You can change the pose by either moving the object with respect to the camera, or the camera with respect to the object.

The pose estimation problem described in this tutorial is often referred to as Perspective-n-Point problem or PNP in computer vision jargon. As we shall see in the following sections in more detail, in this problem the goal is to find the pose of an object when we have a calibrated camera, and we know the locations of n 3D points on the object and the corresponding 2D projections in the image.
How to mathematically represent camera motion ?
A 3D rigid object has only two kinds of motions with respect to a camera.

Translation : Moving the camera from its current 3D location (X, Y, Z) to a new 3D location (X', Y', Z') is called translation. As you can see translation has 3 degrees of freedom — you can move in the X, Y or Z direction. Translation is represented by a vector \mathbf{t} which is equal to ( X' - X, Y' - Y, Z' - Z ).
Rotation : You can also rotate the camera about the X, Y and Z axes. A rotation, therefore, also has three degrees of freedom. There are many ways of representing rotation. You can represent it using Euler angles ( roll, pitch and yaw ), a 3\times3 rotation matrix, or a direction of rotation (i.e. axis ) and angle.
So, estimating the pose of a 3D object means finding 6 numbers — three for translation and three for rotation.
What do you need for pose estimation ?
To calculate the 3D pose of an object in an image you need the following information

2D coordinates of a few points : You need the 2D (x,y) locations of a few points in the image. In the case of a face, you could choose the corners of the eyes, the tip of the nose, corners of the mouth etc. Dlib’s facial landmark detector provides us with many points to choose from. In this tutorial, we will use the tip of the nose, the chin, the left corner of the left eye, the right corner of the right eye, the left corner of the mouth, and the right corner of the mouth.
3D locations of the same points : You also need the 3D location of the 2D feature points. You might be thinking that you need a 3D model of the person in the photo to get the 3D locations. Ideally yes, but in practice, you don’t. A generic 3D model will suffice. Where do you get a 3D model of a head from ? Well, you really don’t need a full 3D model. You just need the 3D locations of a few points in some arbitrary reference frame. In this tutorial, we are going to use the following 3D points.
Tip of the nose : ( 0.0, 0.0, 0.0)
Chin : ( 0.0, -330.0, -65.0)
Left corner of the left eye : (-225.0f, 170.0f, -135.0)
Right corner of the right eye : ( 225.0, 170.0, -135.0)
Left corner of the mouth : (-150.0, -150.0, -125.0)
Right corner of the mouth : (150.0, -150.0, -125.0)
Note that the above points are in some arbitrary reference frame / coordinate system. This is called the World Coordinates ( a.k.a Model Coordinates in OpenCV docs ) .

Intrinsic parameters of the camera. As mentioned before, in this problem the camera is assumed to be calibrated. In other words, you need to know the focal length of the camera, the optical center in the image and the radial distortion parameters. So you need to calibrate your camera. Of course, for the lazy dudes and dudettes among us, this is too much work. Can I supply a hack ? Of course, I can! We are already in approximation land by not using an accurate 3D model. We can approximate the optical center by the center of the image, approximate the focal length by the width of the image in pixels and assume that radial distortion does not exist. Boom! you did not even have to get up from your couch!

There are several algorithms for pose estimation. The first known algorithm dates back to 1841. It is beyond the scope of this post to explain the details of these algorithms but here is a general idea.

There are three coordinate systems in play here. The 3D coordinates of the various facial features shown above are in world coordinates. If we knew the rotation and translation ( i.e. pose ), we could transform the 3D points in world coordinates to 3D points in camera coordinates. The 3D points in camera coordinates can be projected onto the image plane ( i.e. image coordinate system ) using the intrinsic parameters of the camera ( focal length, optical center etc. ).

