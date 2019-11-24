import cv2
from darkflow.net.build import TFNet
import numpy as np
import time
import tensorflow as tf
import serial

target = (320,240)

def trigger(mySerial,state):
    if state:
        mySerial.write(b'1')
    else:
        mySerial.write(b'2')

def displayResults(results, img, mySerial):
    for (i, result) in enumerate(results):
        if result['label']!="person":
            continue
        x = result['topleft']['x']
        w = result['bottomright']['x']-result['topleft']['x']
        y = result['topleft']['y']
        h = result['bottomright']['y']-result['topleft']['y']
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        label_position = (x + int(w/2)), abs(y - 10)
        cv2.putText(img, result['label'], label_position , cv2.FONT_HERSHEY_SIMPLEX,0.5, (255,255,255), 2)

        #cv2.circle(img, target, 5, (255,0,0), 4)

        if x<target[0]<x+w and y<target[1]<y+h:
            trigger(mySerial, True)
        else:
            trigger(mySerial,False)

    return img

if __name__ == "__main__":
    mySerial = serial.Serial()
    mySerial.baudrate = 115200
    mySerial.port = "/dev/ttyUSB0"
    mySerial.open()

    config = tf.compat.v1.ConfigProto(log_device_placement=True)
    config.gpu_options.allow_growth = True

    with tf.compat.v1.Session(config=config) as sess:
        options = {
            'model': './cfg/yolo.cfg',
            'load': './weights/yolov2.weights',
            'threshold': 0.5,
            'gpu': 0.7
        }
        tfnet = TFNet(options)

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()

        cv2.putText(frame, '+', target, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        #print(frame.shape)
        if ret:
            results = tfnet.return_predict(frame)
            image = displayResults(results, frame,mySerial)
            image = cv2.resize(image, (1920, 1080))
            cv2.imshow('Automatic Targetting System', image)
            if cv2.waitKey(1) == 13:  # 13 is the Enter Key
                break

    capture.release()
    cv2.destroyAllWindows()

    mySerial.close()