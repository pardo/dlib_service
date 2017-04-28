# dlib_service

Use dlib face detection and recognition from an API:

```shell
docker build -t dlib .
docker run --rm -p 0.0.0.0:8080:8080 --name running-dlib dlib
```

You can request the service with curl like:

```shell
# get only face detection
curl -F "photo=@my_photo.jpg" localhost:8080/faces
# get face detection + 68 landmark array
curl -F "photo=@my_photo.jpg" localhost:8080/faces-landmarks
# get face detection + 68 landmark + 128 descriptor
curl -F "photo=@my_photo.jpg" localhost:8080/faces-descriptors
```

You can use euclidian distance to know if is the same face or not.

Read more here:
- <http://dlib.net/>
- <http://dlib.net/face_detector.py.html>
- <http://dlib.net/face_landmark_detection.py.html>
- <http://dlib.net/face_recognition.py.html>