import numpy as np
import argparse
import imutils
import cv2


def argument_image():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, help="path to the image file")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])
    return image


def sharpen_image(img1, level):

    b = (1-level)/8
    kernel = np.array([[b, b, b], [b, level, b], [b, b, b]])
    img2 = cv2.filter2D(img1, -1, kernel)
    return img2


def get_image(url):

    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    frame = sharpen_image(frame, 2)

    # cv2.imwrite('a.png', frame)
    # frame = cv2.imread('a.png')
    img_f = cv2.convertScaleAbs(frame, alpha=1, beta=0)
    cap.release()

    return img_f


def put_scale(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized_image


def stream_detect():

    url1 = "http://192.168.137.132:8080/video/mjpeg"
    try:
        image = get_image(0)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # except Exception:
    #     image = get_image('stream')
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    except:
        image = get_image('test')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = put_scale(image, 100)
    image = cv2.convertScaleAbs(image, alpha=2, beta=-50)
    ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=3)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=3)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.blur(gradient, (3, 3))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=1)
    closed = cv2.dilate(closed, None, iterations=1)

    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    try:
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        rect = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)

        box = np.int0(box)
        cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        print(box)

    except:
        print("Nothing found")

    cv2.imshow("frame", image)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        return False

    return True


def run():

    while True:

        key = stream_detect()
        if not key:
            return

    return


cv2.setUseOptimized(True)
run()
print("\n Process ended.")
cv2.destroyAllWindows()
