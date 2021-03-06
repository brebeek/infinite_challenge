import face_recognition

import face_recognition
import cv2
import numpy as np

known_image = face_recognition.load_image_file("dataset/hongchul/00000000.jpg")
unknown_image = face_recognition.load_image_file("dataset/jaesuk/00000002.jpg")

#Adding encoding for the known person 'hongchul'
hongchul_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

# We are comparing the unknown image with the known person 'hongchul'
results = face_recognition.compare_faces([hongchul_encoding], unknown_encoding)
#True: unkown matches the person 'hongchul', else False
print(results)
