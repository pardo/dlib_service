FROM buildpack-deps:jessie

RUN apt-get update && apt-get install -y --no-install-recommends \
  cmake \
  libgtk-3-dev \
  libboost-all-dev \
	&& rm -rf /var/lib/apt/lists/*

RUN wget http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
RUN bzip2 -d dlib_face_recognition_resnet_model_v1.dat.bz2
RUN wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
RUN bzip2 -d shape_predictor_68_face_landmarks.dat.bz2

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py

COPY requirements.txt /
COPY faces.py /

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT python faces.py