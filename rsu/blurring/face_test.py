import numpy as np
import cv2
# 13.jpg
# (xmin, ymin, xmax, ymax)
blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)

# image load
img = cv2.imread('face1.jpg')

# face blurring
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
xml = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)
faces = face_cascade.detectMultiScale(gray, 1.2, 5)
print('Number of faces detected : ', len(faces))
if(len(faces)) :
    for (x, y, w, h) in faces :
        cv2.rectangle(img, (x, y), (x + w, y + h), blue_color, -1)
    cv2.imshow('face', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()