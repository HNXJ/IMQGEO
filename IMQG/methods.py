import cv2
import argparse
import numpy as np
from abc import ABC
import matplotlib.pyplot as plt


font = cv2.FONT_HERSHEY_SIMPLEX
cv2.CAP_PROP_BUFFERSIZE = 100


class StreamBuffer(ABC):

    def __init__(self):

        self.img = None
        self.image_flag = False
        self.camera_url = 0
        return

    def set_img(self, im):

        self.img = im
        if self.img is not None:

            self.image_flag = True

        return

    def get_img(self):

        return self.img


def put_scale(img, scale_percent):

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized_image


def laplacian_filter(img1, level):

    b = (1-level)/8
    kernel = np.array([[b, b, b], [b, level, b], [b, b, b]])
    img2 = cv2.filter2D(img1, -1, kernel)
    return img2


def quad_area(data):

    l = data.shape[0]//2
    corners = data[["c1", "c2", "c3", "c4"]].values.reshape(l, 2,4)

    c1 = corners[:, :, 0]
    c2 = corners[:, :, 1]
    c3 = corners[:, :, 2]
    c4 = corners[:, :, 3]

    e1 = c2-c1
    e2 = c3-c2
    e3 = c4-c3
    e4 = c1-c4

    a = -.5 * (np.cross(-e1, e2, axis = 1) + np.cross(-e3, e4, axis = 1))
    return a


def argument_image():

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the image file")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    return image


def get_image_from_camera(camera_object):

    ret, frame = camera_object.read()
    return frame


def get_contour(input_image):

    img = input_image
    # img = cv2.convertScaleAbs(img, 2, -250)
    try:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    except:
        pass
    threshold, img_bw = cv2.threshold(img, 150, 220, cv2.THRESH_BINARY)
    # cv2.imshow('th', img_bw)
    contours, _ = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_target(contours, img):

    for cnt in contours:

        if cv2.arcLength(cnt, True) < 20 or cv2.contourArea(cnt) < 100:

            continue

        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (255, 0, 0), 1)
        x = int(np.mean(approx[:, 0, 0]))
        y = int(np.mean(approx[:, 0, 1]))

        if len(approx) < 3:
            cv2.putText(img, "Line", (x, y), font, 1, 0)

        elif len(approx) == 3:
            # pass
            cv2.putText(img, "Triangle", (x, y), font, 1, 0)
        elif len(approx) == 4:
            # pass
            cv2.putText(img, "Rectangle", (x, y), font, 1, 0)
        elif len(approx) == 5:
            # pass
            cv2.putText(img, "Pentagon", (x, y), font, 1, 0)
        elif 6 < len(approx) < 15:
            # pass
            cv2.putText(img, "Free Shape", (x, y), font, 1, (0))
        else:
            pass
            cv2.putText(img, "Circle", (x, y), font, 1, (0))

    return img


def shape_detect(input_image, fname="s.png"):

    img = input_image
    cnt = get_contour(img)
    img = get_target(cnt, img)

    # cv2.imshow("shapes", img)
    plt.figure(1)
    imgplot = plt.imshow(img)
    
    plt.show()
    # cv2.imshow("Threshold", img)

    # if key1 and 0xFF == ord('q'):
    #     return False

    # if key1 and 0xFF == ord('s'):
    key1 = input("Save?(y/n)")
    if key1 == "y":
        cv2.imwrite(fname, img)

    return True


def help_mode():

    print('\n--------------------------------------------------------------------\n'
          '         This is QXJ pattern detector 1.0.\n'
          '     1.There are 3 modes; Barcode detector, ArUco pattern detector,and\n'
          '     Shape detector.\n'
          '     enter b for barcode detector, a for ArUco detector and s for sha-\n'
          '     pe detector.\n'
          '     2.There are 4 camera modes; Webcam, phone cam 1,2 and free URLs.,\n'
          '     enter w for webcam, p1 or p2 for phone 1,2 or enter URL address. \n'
          '\n--------------------------------------------------------------------\n')
    return
