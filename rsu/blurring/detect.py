import os
# comment out below line to enable tensorflow outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
import core.utils as utils
from core.yolov4 import filter_boxes
from core.functions import *
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from skimage import io

#flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
#flags.DEFINE_string('weights', './checkpoints/custom-416','path to weights file')
#flags.DEFINE_integer('size', 416, 'resize images to')
#flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
#flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
#flags.DEFINE_list('images', './data/images/car.jpg', 'path to input image')
#flags.DEFINE_string('output', './detections/', 'path to output folder')
#flags.DEFINE_float('iou', 0.45, 'iou threshold')
#flags.DEFINE_float('score', 0.50, 'score threshold')
#flags.DEFINE_boolean('info', False, 'print info on detections')
#flags.DEFINE_boolean('crop', False, 'crop detections from images')
#flags.DEFINE_boolean('plate', False, 'perform license plate recognition')

def detect(image_path):
    loc_list = []
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    #STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)

    framework = 'tf'
    weights = './checkpoints/custom-416'
    size = 416
    tiny = False
    model = 'yolov4'
    output = './detections/'
    iou = 0.45
    score = 0.50
    info = False
    crop = False
    plate = False

    input_size = size
    images = image_path

    # load model
    if framework == 'tflite':
            interpreter = tf.lite.Interpreter(model_path=weights)
    else:
            saved_model_loaded = tf.saved_model.load(weights, tags=[tag_constants.SERVING])

    # loop through images in list and run Yolov4 model on each
    for i in range (1):
        original_image = io.imread(images)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.
        
        # get image name by using split method
        image_name = image_path.split('/')[-1]
        image_name = image_name.split('.')[0]

        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)

        if framework == 'tflite':
            interpreter.allocate_tensors()
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            interpreter.set_tensor(input_details[0]['index'], images_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            if model == 'yolov3' and tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25, input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([input_size, input_size]))
        else:
            infer = saved_model_loaded.signatures['serving_default']
            batch_data = tf.constant(images_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        # run non max suppression on detections
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou,
            score_threshold=score
        )

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = original_image.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)
        
        # hold all detection data in one variable
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())

        image = utils.draw_bbox(original_image, pred_bbox, info, allowed_classes=allowed_classes, read_plate = plate)
        loc_list += obtain_coordinates(str(images), pred_bbox)
    return loc_list
        #image = Image.fromarray(image.astype(np.uint8))
        #image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        #cv2.imwrite(output + 'detection' + str(count) + '.png', image)

def obtain_coordinates(img, data):
    coordinates = []
    boxes, scores, classes, num_objects = data
    for i in range(num_objects):
        xmin, ymin,xmax, ymax = boxes[i]
        coordinates.append((int(xmin), int(ymin),int(xmax), int(ymax)))
    return coordinates

def detect_ip(image_path):
    print(detect(image_path))
    return detect(image_path)

# if __name__ == '__main__':
#     try:
#         detect_ip("./data/images/car.jpg")# image_path
#     except SystemExit:
#         pass
