import numpy as np
import cv2.cv2 as cv2
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from IMQMethods import *
from PIL import Image 
import sys 
from pdf2image import convert_from_path 
import os 
    

def pdf_converter(PDF_file="d.pdf"):
      
    pages = convert_from_path(PDF_file, 500) 
    image_counter = 1
      
    for page in pages: 
        filename = PDF_file[:-4] + "_page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
    
    return


def channels(I1=None, mode="default", scale_percent=20, filepath = 'CyprusGeologyMapTaurus.tif'):
    
    if filepath[-3:] == "pdf":
        pdf_converter(filepath)
        print("PDF file converted.")
        I1 = cv2.imread(filepath[:-4] + "page_" + str(1) + ".jpg")
   
    else:
        I1 = cv2.imread(filepath)

    print('Image loaded...')
    
    if mode == 'manual':
        scale_percent = float(input('Resize scale? (0-100)'))
    
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    kernel = np.ones((3, 3), np.uint8)  
    dim = (width, height)
    
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I2 = cv2.cvtColor(I2, cv2.COLOR_RGB2BGR)
    
    d_min = (0, 0, 0)
    d_max = (90, 90, 90)
    I_dark = cv2.inRange(I2, d_min, d_max)
    I_dark = cv2.dilate(I_dark, kernel, iterations=3) 
    
    I3 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I3[:, :, 0] = I2[:, :, 0] - np.multiply(I2[:, :, 0], I_dark/255)
    I3[:, :, 1] = I2[:, :, 1] - np.multiply(I2[:, :, 1], I_dark/255)
    I3[:, :, 2] = I2[:, :, 2] - np.multiply(I2[:, :, 2], I_dark/255)
    
    r_min = (80, 120, 80)
    r_max = (200, 150, 120)
    I_red = cv2.inRange(I3, r_min, r_max)
    I_red = cv2.dilate(I_red, kernel, iterations=3) 
    
    I4 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I4[:, :, 0] = I3[:, :, 0] - np.multiply(I3[:, :, 0], I_red/255)
    I4[:, :, 1] = I3[:, :, 1] - np.multiply(I3[:, :, 1], I_red/255)
    I4[:, :, 2] = I3[:, :, 2] - np.multiply(I3[:, :, 2], I_red/255)
    
    I3 = I4
    
    b_min = (160, 160, 200)
    b_max = (200, 200, 255)
    I_blue = cv2.inRange(I3, b_min, b_max)
    # I_blue = cv2.erode(I_blue, kernel, iterations=1)
    I_blue = cv2.dilate(I_blue, kernel, iterations=4) 
    I_blue = cv2.medianBlur(I_blue, ksize=5)
    
    b_min2 = (30, 30, 90)
    b_max2 = (90, 90, 200)
    I_blue2 = cv2.inRange(I3, b_min2, b_max2)
    # I_blue2 = cv2.erode(I_blue2, kernel, iterations=1)
    I_blue2 = cv2.dilate(I_blue2, kernel, iterations=4) 
    I_blue2 = cv2.medianBlur(I_blue2, ksize=5)
    
    print('Color hard thresholding done.')
    
    print('Detection phase...')
    # shape_detect(cv2.cvtColor(I_pink, cv2.COLOR_GRAY2RGB), "pinks.png")
    # shape_detect(cv2.cvtColor(I_dark, cv2.COLOR_GRAY2RGB), "darks.png")
    # shape_detect(cv2.cvtColor(I_blue, cv2.COLOR_GRAY2RGB), "lblues.png")
    I = shape_detect(cv2.cvtColor(I_blue2, cv2.COLOR_GRAY2RGB), "dblues.png")
    # shape_detect(cv2.cvtColor(I_red, cv2.COLOR_GRAY2RGB), "rednoises.png")
    
    return I


def Borders(I1=None, mode="default", scale_percent=20, filepath = 'CyprusGeologyMapTaurus.tif'):
    
    if filepath[-3:] == "pdf":
        pdf_converter(filepath)
        print("PDF file converted.")
        I1 = cv2.imread(filepath[:-4] + "page_" + str(1) + ".jpg")
   
    else:
        I1 = cv2.imread(filepath)

    print('Image loaded...')
    
    if mode == 'manual':
        scale_percent = float(input('Resize scale? (0-100)'))
    
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    kernel = np.ones((3, 3), np.uint8)  
    dim = (width, height)
    
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I2 = cv2.cvtColor(I2, cv2.COLOR_RGB2BGR)
    
    d_min = (0, 0, 0)
    d_max = (90, 90, 90)
    I_dark = cv2.inRange(I2, d_min, d_max)
    I_dark = cv2.dilate(I_dark, kernel, iterations=3) 
    
    I3 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I3[:, :, 0] = I2[:, :, 0] - np.multiply(I2[:, :, 0], I_dark/255)
    I3[:, :, 1] = I2[:, :, 1] - np.multiply(I2[:, :, 1], I_dark/255)
    I3[:, :, 2] = I2[:, :, 2] - np.multiply(I2[:, :, 2], I_dark/255)
    
    r_min = (80, 120, 80)
    r_max = (200, 150, 120)
    I_red = cv2.inRange(I3, r_min, r_max)
    I_red = cv2.dilate(I_red, kernel, iterations=3) 
    
    I4 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I4[:, :, 0] = I3[:, :, 0] - np.multiply(I3[:, :, 0], I_red/255)
    I4[:, :, 1] = I3[:, :, 1] - np.multiply(I3[:, :, 1], I_red/255)
    I4[:, :, 2] = I3[:, :, 2] - np.multiply(I3[:, :, 2], I_red/255)
    
    I3 = I4
    
    b_min = (160, 160, 200)
    b_max = (200, 200, 255)
    I_blue = cv2.inRange(I3, b_min, b_max)
    # I_blue = cv2.erode(I_blue, kernel, iterations=1)
    I_blue = cv2.dilate(I_blue, kernel, iterations=4) 
    I_blue = cv2.medianBlur(I_blue, ksize=5)
    
    b_min2 = (30, 30, 90)
    b_max2 = (90, 90, 200)
    I_blue2 = cv2.inRange(I3, b_min2, b_max2)
    # I_blue2 = cv2.erode(I_blue2, kernel, iterations=1)
    I_blue2 = cv2.dilate(I_blue2, kernel, iterations=4) 
    I_blue2 = cv2.medianBlur(I_blue2, ksize=5)
    
    p_min = (180, 100, 150)
    p_max = (220, 140, 180)
    I_pink = cv2.inRange(I3, p_min, p_max)
    I_pink = cv2.dilate(I_pink, kernel, iterations=3)
    
    print('Color hard thresholding done.')
    
    # img_erosion = cv2.erode(img, kernel, iterations=1)
    # laplaceKernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # I_b = cv2.filter2D(I_b, -1, laplaceKernel)
    
    print('Detection phase...')
    # shape_detect(cv2.cvtColor(I_pink, cv2.COLOR_GRAY2RGB), "pinks.png")
    I = shape_detect(cv2.cvtColor(I_dark, cv2.COLOR_GRAY2RGB), "darks.png")
    # shape_detect(cv2.cvtColor(I_blue, cv2.COLOR_GRAY2RGB), "lblues.png")
    # shape_detect(cv2.cvtColor(I_blue2, cv2.COLOR_GRAY2RGB), "dblues.png")
    # shape_detect(cv2.cvtColor(I_red, cv2.COLOR_GRAY2RGB), "rednoises.png")
    
    # plt.figure('Dark parts')
    # imgplot = plt.imshow(I_dark)
    # plt.show()
    return I


def Rivers(I1=None, mode="default", scale_percent=20, filepath = 'CyprusGeologyMapTaurus.tif'):
    
    if filepath[-3:] == "pdf":
        pdf_converter(filepath)
        print("PDF file converted.")
        I1 = cv2.imread(filepath[:-4] + "page_" + str(1) + ".jpg")
   
    else:
        I1 = cv2.imread(filepath)

    print('Image loaded...')
    
    if mode == 'manual':
        scale_percent = float(input('Resize scale? (0-100)'))
    
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    kernel = np.ones((3, 3), np.uint8)  
    dim = (width, height)
    
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I2 = cv2.cvtColor(I2, cv2.COLOR_RGB2BGR)
    
    d_min = (0, 0, 0)
    d_max = (90, 90, 90)
    I_dark = cv2.inRange(I2, d_min, d_max)
    I_dark = cv2.dilate(I_dark, kernel, iterations=3) 
    
    I3 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I3[:, :, 0] = I2[:, :, 0] - np.multiply(I2[:, :, 0], I_dark/255)
    I3[:, :, 1] = I2[:, :, 1] - np.multiply(I2[:, :, 1], I_dark/255)
    I3[:, :, 2] = I2[:, :, 2] - np.multiply(I2[:, :, 2], I_dark/255)
    
    r_min = (80, 120, 80)
    r_max = (200, 150, 120)
    I_red = cv2.inRange(I3, r_min, r_max)
    I_red = cv2.dilate(I_red, kernel, iterations=3) 
    
    I4 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I4[:, :, 0] = I3[:, :, 0] - np.multiply(I3[:, :, 0], I_red/255)
    I4[:, :, 1] = I3[:, :, 1] - np.multiply(I3[:, :, 1], I_red/255)
    I4[:, :, 2] = I3[:, :, 2] - np.multiply(I3[:, :, 2], I_red/255)
    
    I3 = I4
    
    b_min = (160, 160, 200)
    b_max = (200, 200, 255)
    I_blue = cv2.inRange(I3, b_min, b_max)
    # I_blue = cv2.erode(I_blue, kernel, iterations=1)
    I_blue = cv2.dilate(I_blue, kernel, iterations=4) 
    I_blue = cv2.medianBlur(I_blue, ksize=5)
    
    b_min2 = (30, 30, 90)
    b_max2 = (90, 90, 200)
    I_blue2 = cv2.inRange(I3, b_min2, b_max2)
    # I_blue2 = cv2.erode(I_blue2, kernel, iterations=1)
    I_blue2 = cv2.dilate(I_blue2, kernel, iterations=4) 
    I_blue2 = cv2.medianBlur(I_blue2, ksize=5)
    
    p_min = (180, 100, 150)
    p_max = (220, 140, 180)
    I_pink = cv2.inRange(I3, p_min, p_max)
    I_pink = cv2.dilate(I_pink, kernel, iterations=3)
    
    print('Color hard thresholding done.')
    
    # img_erosion = cv2.erode(img, kernel, iterations=1)
    # laplaceKernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # I_b = cv2.filter2D(I_b, -1, laplaceKernel)
    
    print('Detection phase...')
    # shape_detect(cv2.cvtColor(I_pink, cv2.COLOR_GRAY2RGB), "pinks.png")
    # I = shape_detect(cv2.cvtColor(I_dark, cv2.COLOR_GRAY2RGB), "darks.png")
    I = shape_detect(cv2.cvtColor(I_blue, cv2.COLOR_GRAY2RGB), "lblues.png")
    # shape_detect(cv2.cvtColor(I_blue2, cv2.COLOR_GRAY2RGB), "dblues.png")
    # shape_detect(cv2.cvtColor(I_red, cv2.COLOR_GRAY2RGB), "rednoises.png")
    
    # plt.figure('Dark parts')
    # imgplot = plt.imshow(I_dark)
    # plt.show()
    return I


def Roads(I1=None, mode="default", scale_percent=20, filepath = 'CyprusGeologyMapTaurus.tif'):
    
    if filepath[-3:] == "pdf":
        pdf_converter(filepath)
        print("PDF file converted.")
        I1 = cv2.imread(filepath[:-4] + "page_" + str(1) + ".jpg")
   
    else:
        I1 = cv2.imread(filepath)

    print('Image loaded...')
    
    
    if mode == 'manual':
        scale_percent = float(input('Resize scale? (0-100)'))
    
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    kernel = np.ones((3, 3), np.uint8)  
    dim = (width, height)
    
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I2 = cv2.cvtColor(I2, cv2.COLOR_RGB2BGR)
    
    d_min = (0, 0, 0)
    d_max = (90, 90, 90)
    I_dark = cv2.inRange(I2, d_min, d_max)
    I_dark = cv2.dilate(I_dark, kernel, iterations=3) 
    
    I3 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I3[:, :, 0] = I2[:, :, 0] - np.multiply(I2[:, :, 0], I_dark/255)
    I3[:, :, 1] = I2[:, :, 1] - np.multiply(I2[:, :, 1], I_dark/255)
    I3[:, :, 2] = I2[:, :, 2] - np.multiply(I2[:, :, 2], I_dark/255)
    
    r_min = (80, 120, 80)
    r_max = (200, 150, 120)
    I_red = cv2.inRange(I3, r_min, r_max)
    I_red = cv2.dilate(I_red, kernel, iterations=3) 
    
    I4 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I4[:, :, 0] = I3[:, :, 0] - np.multiply(I3[:, :, 0], I_red/255)
    I4[:, :, 1] = I3[:, :, 1] - np.multiply(I3[:, :, 1], I_red/255)
    I4[:, :, 2] = I3[:, :, 2] - np.multiply(I3[:, :, 2], I_red/255)
    
    I3 = I4
    
    b_min = (160, 160, 200)
    b_max = (200, 200, 255)
    I_blue = cv2.inRange(I3, b_min, b_max)
    # I_blue = cv2.erode(I_blue, kernel, iterations=1)
    I_blue = cv2.dilate(I_blue, kernel, iterations=4) 
    I_blue = cv2.medianBlur(I_blue, ksize=5)
    
    b_min2 = (30, 30, 90)
    b_max2 = (90, 90, 200)
    I_blue2 = cv2.inRange(I3, b_min2, b_max2)
    # I_blue2 = cv2.erode(I_blue2, kernel, iterations=1)
    I_blue2 = cv2.dilate(I_blue2, kernel, iterations=4) 
    I_blue2 = cv2.medianBlur(I_blue2, ksize=5)
    
    p_min = (180, 100, 150)
    p_max = (220, 140, 180)
    I_pink = cv2.inRange(I3, p_min, p_max)
    I_pink = cv2.dilate(I_pink, kernel, iterations=3)
    
    print('Color hard thresholding done.')
    
    # img_erosion = cv2.erode(img, kernel, iterations=1)
    # laplaceKernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # I_b = cv2.filter2D(I_b, -1, laplaceKernel)
    
    print('Detection phase...')
    I = shape_detect(cv2.cvtColor(I_pink, cv2.COLOR_GRAY2RGB), "pinks.png")
    # I = shape_detect(cv2.cvtColor(I_dark, cv2.COLOR_GRAY2RGB), "darks.png")
    # I = shape_detect(cv2.cvtColor(I_blue, cv2.COLOR_GRAY2RGB), "lblues.png")
    # shape_detect(cv2.cvtColor(I_blue2, cv2.COLOR_GRAY2RGB), "dblues.png")
    # shape_detect(cv2.cvtColor(I_red, cv2.COLOR_GRAY2RGB), "rednoises.png")
    
    # plt.figure('Dark parts')
    # imgplot = plt.imshow(I_dark)
    # plt.show()
    return I


def R(I1, mode="default", scale_percent=20):
    print('Image loaded...')
    mode = str(input('Mode? (default, manual)'))
    
    if mode == 'manual':
        scale_percent = float(input('Resize scale? (0-100)'))
    
    width = int(I1.shape[1] * scale_percent / 100)
    height = int(I1.shape[0] * scale_percent / 100)
    kernel = np.ones((3, 3), np.uint8)  
    dim = (width, height)
    
    I2 = cv2.resize(I1[:, :, :], dim, interpolation = cv2.INTER_AREA)
    I2 = cv2.cvtColor(I2, cv2.COLOR_RGB2BGR)
    
    d_min = (0, 0, 0)
    d_max = (90, 90, 90)
    I_dark = cv2.inRange(I2, d_min, d_max)
    I_dark = cv2.dilate(I_dark, kernel, iterations=3) 
    
    I3 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I3[:, :, 0] = I2[:, :, 0] - np.multiply(I2[:, :, 0], I_dark/255)
    I3[:, :, 1] = I2[:, :, 1] - np.multiply(I2[:, :, 1], I_dark/255)
    I3[:, :, 2] = I2[:, :, 2] - np.multiply(I2[:, :, 2], I_dark/255)
    
    r_min = (80, 120, 80)
    r_max = (200, 150, 120)
    I_red = cv2.inRange(I3, r_min, r_max)
    I_red = cv2.dilate(I_red, kernel, iterations=3) 
    
    I4 = np.zeros((I_dark.shape[0], I_dark.shape[1], 3), dtype=np.uint8)
    I4[:, :, 0] = I3[:, :, 0] - np.multiply(I3[:, :, 0], I_red/255)
    I4[:, :, 1] = I3[:, :, 1] - np.multiply(I3[:, :, 1], I_red/255)
    I4[:, :, 2] = I3[:, :, 2] - np.multiply(I3[:, :, 2], I_red/255)
    
    I3 = I4
    
    b_min = (160, 160, 200)
    b_max = (200, 200, 255)
    I_blue = cv2.inRange(I3, b_min, b_max)
    # I_blue = cv2.erode(I_blue, kernel, iterations=1)
    I_blue = cv2.dilate(I_blue, kernel, iterations=4) 
    I_blue = cv2.medianBlur(I_blue, ksize=5)
    
    b_min2 = (30, 30, 90)
    b_max2 = (90, 90, 200)
    I_blue2 = cv2.inRange(I3, b_min2, b_max2)
    # I_blue2 = cv2.erode(I_blue2, kernel, iterations=1)
    I_blue2 = cv2.dilate(I_blue2, kernel, iterations=4) 
    I_blue2 = cv2.medianBlur(I_blue2, ksize=5)
    
    p_min = (180, 100, 150)
    p_max = (220, 140, 180)
    I_pink = cv2.inRange(I3, p_min, p_max)
    I_pink = cv2.dilate(I_pink, kernel, iterations=3)
    
    print('Color hard thresholding done.')
    
    # img_erosion = cv2.erode(img, kernel, iterations=1)
    # laplaceKernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # I_b = cv2.filter2D(I_b, -1, laplaceKernel)
    
    print('Detection phase...')
    # shape_detect(cv2.cvtColor(I_pink, cv2.COLOR_GRAY2RGB), "pinks.png")
    # shape_detect(cv2.cvtColor(I_dark, cv2.COLOR_GRAY2RGB), "darks.png")
    shape_detect(cv2.cvtColor(I_blue, cv2.COLOR_GRAY2RGB), "lblues.png")
    shape_detect(cv2.cvtColor(I_blue2, cv2.COLOR_GRAY2RGB), "dblues.png")
    # shape_detect(cv2.cvtColor(I_red, cv2.COLOR_GRAY2RGB), "rednoises.png")
    
    # plt.figure('Dark parts')
    # imgplot = plt.imshow(I_dark)
    # plt.show()
    return

# filepath = str(input('Filepath:\n(d for default)'))
# if filepath == 'd':
#     filepath = 'CyprusGeologyMapTaurus.tif'
    
# I1 = cv2.imread(filepath)
# run(I1)
