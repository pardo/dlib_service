import dlib
import math
import json

from skimage import io
from bottle import route, run, request

predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'

# Load all the models we need: a detector to find the faces, a shape predictor
# to find face landmarks so we can precisely localize the face, and finally the
# face recognition model.
detector = dlib.get_frontal_face_detector()
face_landmark_predictor = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def euclidean(vector1, vector2):
    '''
    calculate the euclidean distance, no numpy
    input: numpy.arrays or lists
    return: euclidean distance
    '''
    dist = [(a - b)**2 for a, b in zip(vector1, vector2)]
    dist = math.sqrt(sum(dist))
    return dist


def analyze(photo, do_landmark=False, do_face_descriptor=False):
    img = io.imread(photo.file)
    dets = detector(img)
    print("Number of faces detected: {}".format(len(dets)))
    result = []
    # Now process each face we found.
    for box in dets:
        data = { 
            "filename": photo.filename,
            "class": "face",
            "probability": None, 
            "left": box.left(),
            "top": box.top(),
            "right": box.right(),
            "bottom": box.bottom()
        }

        if do_landmark or do_face_descriptor:
            shape = face_landmark_predictor(img, box)
            data["landmark_68"] = list(map(lambda x: (x.x, x.y), shape.parts()))
            if do_face_descriptor:
                face_descriptor = facerec.compute_face_descriptor(img, shape)
                data["face_descriptor"] = [ x for x in face_descriptor ]

        result.append(data)
    return json.dumps(result)


@route('/faces', method='POST')
def index_view():
    photo = request.files.get('photo')
    return analyze(photo)

@route('/faces-landmarks', method='POST')
def index_view():
    photo = request.files.get('photo')
    return analyze(photo, True)
    
@route('/faces-descriptors', method='POST')
def index_view():
    photo = request.files.get('photo')
    return analyze(photo, True, True)

run(host='0.0.0.0', port=8080)