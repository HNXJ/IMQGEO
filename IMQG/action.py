import numpy as np
import cv2.cv2 as cv2
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt


def rect(x, th):    
    return (np.ceil((np.abs(x) + x)/2) > th)*255


def on_button_clicked(ratio_):
    I1 = cv2.imread('CyprusGeologyMapTaurus.tif')
    
    scale_percent = ratio_
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    dim = (width, height)
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I3 = rect(I2[:, :, 2] - I2[:, :, 0], 100)
    plt.figure(1)
    imgplot = plt.imshow(I2)  
    # plt.show()

    plt.figure(2)
    imgplot = plt.imshow(I3)
    plt.show()
    
    return 
    

def run_demo():
    app = QApplication([])
    button = QPushButton('Click to show image')
    button.clicked.connect(on_button_clicked(20))
    button.show()
    app.exec_()


# on_button_clicked(10)
run_demo()