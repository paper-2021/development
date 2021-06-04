import numpy as np
import cv2

blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)

def blurring(image, locations) : # image name & lp location
    try :
        # LP blurring
        img = cv2.imread(image) # read image by image_path(image)
        for loc in locations :
            x_min, y_min, x_max, y_max = int(loc[0]), int(loc[1]), int(loc[2]), int(loc[3])
            img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), blue_color, -1)

        # face blurring
        frontalface_xml = 'haarcascade_frontalface_default.xml'
        fullbody_xml = 'haarcascade_fullbody.xml'

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_cascade = cv2.CascadeClassifier(frontalface_xml)
        cascade_result = img_cascade.detectMultiScale(gray, 1.2, 5)
        print('Number of faces detected : ', len(cascade_result))
        if(len(cascade_result)) :
            for (x, y, w, h) in cascade_result :
                cv2.rectangle(img, (x, y), (x + w, y + h), blue_color, -1)
        
        image_name = 'b_' + image
        cv2.imwrite(image_name, img)
        return image_name
    except Exception as e :
        print('blurring e : ', e)
        return False

# bound = bouding_box()
# image = ['13.jpg', (487.0, 332.0, 533.0, 349.0)] # lp only
# image = ['6.jpg', (760.0, 709.0, 826.0, 734.0)] # face + lp
# image = ['both1.jpg', (372.0, 333.0, 400.0, 346.0)]
# image = ['both2.jpg', (78.0, 313.0, 138.0, 334.0)]