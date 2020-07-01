import os
import sys
import cv2
import time
from threading import Thread
# from Detectors.methods import *
print(sys.path[0])
sys.path.append(os.path.join(sys.path[0]))
from methods import *
# from distutils.core import setup
# import py2exe
# setup(console=['hello.py'])

url0 = 0
url1 = "http://192.168.1.103:8080/video/mjpeg"
# url2 = "http://192.168.1.5:8080/video/mjpeg"
url2 = "http://192.168.43.190:8080/video/mjpeg"


def run1():

    print("Video stream started.")
    cam1 = cv2.VideoCapture(db.camera_url)
    while True:

        try:

            _, last_img = cam1.read()
            db.set_img(last_img)

        except:

            break

    return


def run2():

    last_time = 0
    cv_error_flag = False
    while True:

        try:
            key = aruco_detect(db.get_img())
            # print(cv2.CAP_PROP_BUFFERSIZE)
            current_time = time.time()
            delay_time = current_time - last_time

            t2 = max(0.0, 0.08 - delay_time)
            time.sleep(t2)

            os.system('cls')
            print(" ==> ArUco pattern FPS monitor\n")
            print(" ==> Process FPS : " + str(1 / (time.time() - last_time)))

            last_time = time.time()

            if not key:
                break

            if cv_error_flag:
                cv_error_flag = False
                print(' ==> Camera available.')

        except cv2.error:

            if not cv_error_flag and not db.image_flag:
                print(' ==> No image available, check camera.')
                cv_error_flag = True

    cap = cv2.VideoCapture(url0)
    cap.release()
    os.system('cls')
    print(' ==> End.\n')
    print(' ----------> QXJ <---------- \n'
          ' -> Credit to PyZbar, Aruco, OpenCV2, Python \n')

    quit()
    return


def run3():
    last_time = 0
    cv_error_flag = False
    while True:

        try:
            key = barcode_detect(db.get_img())
            # print(cv2.CAP_PROP_BUFFERSIZE)
            current_time = time.time()
            delay_time = current_time - last_time

            t2 = max(0.0, 0.08 - delay_time)
            time.sleep(t2)
            os.system('cls')
            print(" ==> Barcode mode FPS monitor\n")
            print(" ==> Process FPS : " + str(1 / (time.time() - last_time)))
            last_time = time.time()

            if not key:
                break

            if cv_error_flag:
                cv_error_flag = False
                print(' ==> Camera available.')

        except cv2.error:

            if not cv_error_flag and not db.image_flag:
                print(' ==> No image available, check camera.')
                cv_error_flag = True

    cap = cv2.VideoCapture(url0)
    cap.release()
    os.system('cls')
    print(' ==> End.\n')
    print(' ----------> QXJ <---------- \n'
          ' -> Credit to PyZbar, Aruco, OpenCV2, Python \n')

    quit()
    return


def run4():
    last_time = 0
    cv_error_flag = False
    while True:

        try:
            key = shape_detect(db.get_img())
            # print(cv2.CAP_PROP_BUFFERSIZE)
            current_time = time.time()
            delay_time = current_time - last_time

            t2 = max(0.0, 0.08 - delay_time)
            time.sleep(t2)
            os.system('cls')
            print(" ==> Barcode mode FPS monitor\n")
            print(" ==> Process FPS : " + str(1 / (time.time() - last_time)))
            last_time = time.time()

            print(key)
            if not key:
                break

            if cv_error_flag:
                cv_error_flag = False
                print(' ==> Camera available.')

        except cv2.error:

            if not cv_error_flag and not db.image_flag:
                print(' ==> No image available, check camera.')
                cv_error_flag = True

    cap = cv2.VideoCapture(url0)
    cap.release()
    os.system('cls')
    print(' ==> End.\n')
    print(' ----------> QXJ <---------- \n'
          ' -> Credit to PyZbar, Aruco, OpenCV2, Python \n')

    quit()
    return


cv2.setUseOptimized(True)
db = StreamBuffer()
print(' ----------> QXJ <---------- \n'
      ' -> Credit to PyZbar, Aruco, OpenCV2, Python \n')

dm1 = input(' --> Do you want to enter help? (y/n)\n -> ')
if dm1 == 'y':
    help_mode()

dm2 = input(' --> Detection camera? (w/p1/p2/URL)\n -> ')
if dm2 == 'w':
    camera_url = url0
elif dm2 == 'p1':
    camera_url = url1
elif dm2 == 'p2':
    camera_url = url2
else:
    camera_url = dm2

db.camera_url = camera_url
dm3 = input(' --> Detection mode? (a/b/s)\n -> ')
if dm3 == 'a':

    t = Thread(target=run1)
    t.start()
    t = Thread(target=run2)
    t.start()

elif dm3 == 'b':

    t = Thread(target=run1)
    t.start()
    t = Thread(target=run3)
    t.start()

elif dm3 == 's':

    t = Thread(target=run1)
    t.start()
    t = Thread(target=run4)
    t.start()

else:
    print(' ==> That mode does not exists. \n')
    exit()

cv2.destroyAllWindows()
