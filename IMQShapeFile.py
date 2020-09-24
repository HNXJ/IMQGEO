import cv2
import csv


def run(filepath=""):
    I = cv2.imread(filepath)
    try:
        I = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
    except:
        print("Already Gray")
    
    fname = filepath[5:8] + "_shapes.csv"
    with open(fname, 'w', newline='') as file:
        fieldnames = ['X', 'Y']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        writer.writeheader()
        for i in range(I.shape[0]):
            for j in range(I.shape[1]):
                if I[i, j] > 200:
                    writer.writerow({'X': i, 'Y': j})
        print("Done, saved in : " + fname)
    return fname
