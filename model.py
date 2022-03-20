import face_recognition
import cv2
import numpy as np
import os


def face(train,test,name):

    image = face_recognition.load_image_file(train) #load image
    image_face_encoding = face_recognition.face_encodings(image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        image_face_encoding,
    ]
    known_face_names = [
        "",# name fform database
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    small_frame = cv2.resize(test, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        face_names.append(name)
    return face_names
