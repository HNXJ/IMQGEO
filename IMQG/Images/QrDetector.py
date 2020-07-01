from __future__ import print_function
from Detectors.methods import *
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2

url0 = 0
url1 = "http://192.168.137.132:8080/video/mjpeg"
url2 = "http://192.168.1.5:8080/video/mjpeg"

cv2.CAP_PROP_BUFFERSIZE = 100
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(url2)


def decoder(im):

    qr_objects = pyzbar.decode(im)
    for i in qr_objects:
        print('Type -> ', i.type, ' | Data : ', i.data, '\n')
    return qr_objects


def barcode_detect():

    ret, frame = cap.read()
    # frame = get_image(cap)
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    code_objects = decoder(im)

    for i in code_objects:
        points = i.polygon

        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(0, n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (255, 0, 0), 3)

        x = i.rect.left
        y = i.rect.top

        print(x, y)
        current_barcode = str(i.data)
        cv2.putText(frame, current_barcode, (x, y), font, 1, (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        return False
    elif key & 0xFF == ord('s'):  # wait for 's' key to save
        cv2.imwrite('SavedCode.png', frame)

    return True


def run():

    while True:

        key = barcode_detect()
        if not key:
            return

    return


run()
cap.release()
cv2.destroyAllWindows()
