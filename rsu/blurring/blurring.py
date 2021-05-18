import numpy as np
import cv2
# 13.jpg
# (xmin, ymin, xmax, ymax)
blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)

# bound = bouding_box()
# image = ['13.jpg', (487.0, 332.0, 533.0, 349.0)] # lp only
# image = ['6.jpg', (760.0, 709.0, 826.0, 734.0)] # face + lp
# image = ['both1.jpg', (372.0, 333.0, 400.0, 346.0)]
# image = ['both2.jpg', (78.0, 313.0, 138.0, 334.0)]
image = ['both3.jpg', (118.0, 258.0, 201.0, 290.0)] # test img
frontalface_xml = 'haarcascade_frontalface_default.xml'
fullbody_xml = 'haarcascade_fullbody.xml'

# image load
img = cv2.imread(image[0])
# license plate blurring
locations = image[1:]
for loc in locations :
    x_min, y_min, x_max, y_max = int(loc[0]), int(loc[1]), int(loc[2]), int(loc[3])
    img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), blue_color, -1)
cv2.imshow('lp', img)
cv2.waitKey(0) # push any key
cv2.destroyAllWindows()

# face blurring
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_cascade = cv2.CascadeClassifier(fullbody_xml)
cascade_result = img_cascade.detectMultiScale(gray, 1.2, 5)
print('Number of faces detected : ', len(cascade_result))
if(len(cascade_result)) :
    for (x, y, w, h) in cascade_result :
        cv2.rectangle(img, (x, y), (x + w, y + h), blue_color, -1)
cv2.imshow('cascade_result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()