import numpy as np
import cv2
from skimage import io

blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)

def blurring(image, locations) : # image name & lp location
    try :
        # LP blurring
        print('image path : ', image)
        img = io.imread(image) # read image by image_path(image)
        for loc in locations :
            x_min, y_min, x_max, y_max = int(loc[0]), int(loc[1]), int(loc[2]), int(loc[3])
            img = cv2.rectangle(img, (x_min, y_min), (x_max, y_max), blue_color, -1)

        # face blurring
        image_path_split = image.split('/')
        path = '/'.join(image_path_split[:-2])
        frontalface_xml = path + '/haarcascade_frontalface_default.xml'
        print('xml path : ', frontalface_xml)
        fullbody_xml = 'haarcascade_fullbody.xml'

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_cascade = cv2.CascadeClassifier(frontalface_xml)
        cascade_result = img_cascade.detectMultiScale(gray, 1.2, 5)
        print('Number of faces detected : ', len(cascade_result))
        if(len(cascade_result)) :
            for (x, y, w, h) in cascade_result :
                cv2.rectangle(img, (x, y), (x + w, y + h), blue_color, -1)
                
        acc_type = image_path_split[-2]
        image_name = str(acc_type) + '_' + 'b_' + image_path_split[-1]
        io.imsave('/'.join(image_path_split[:-1]) + '/' + image_name, img)
        return image_name
    except Exception as e :
        print('blurring e : ', e)
        return False