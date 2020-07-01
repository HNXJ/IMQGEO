import numpy as np
import cv2
font = cv2.FONT_HERSHEY_COMPLEX


def get_image():

    cap = cv2.VideoCapture(0)
    r, img = cap.read()
    img = cv2.convertScaleAbs(img, alpha=2, beta=-50)
    return img


def get_contour(input_image):

    img = cv2.cvtColor(input_image, cv2.COLOR_RGB2GRAY)
    threshold, img_bw = cv2.threshold(img, 200, 205, cv2.THRESH_BINARY)
    # print(img_bw.shape)
    contours, _ = cv2.findContours(img_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_target(contours, img):

    for cnt in contours:

        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if len(approx) == 3:
            cv2.putText(img, "Triangle", (x, y), font, 1, (0))
        elif len(approx) == 4:
            cv2.putText(img, "Rectangle", (x, y), font, 1, (0))
        elif len(approx) == 5:
            cv2.putText(img, "Pentagon", (x, y), font, 1, (0))
        elif 6 < len(approx) < 15:
            cv2.putText(img, "Ellipse", (x, y), font, 1, (0))
        else:
            cv2.putText(img, "Circle", (x, y), font, 1, (0))

    return img


def stream_detect():

    img = db.get_image()
    cnt = get_contour(img)
    img = get_target(cnt, img)

    cv2.imshow("shapes", img)
    # cv2.imshow("Threshold", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return


stream_detect()
