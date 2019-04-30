#!/usr/bin/env python

'''
this project is to create a labelled dataset for binary classification

this program retrieves imgs from train_path
stores roi on mouse clk (@ top-left corner)

this program is run on true class examples
change 1 -> 0 in line 51 for images of false class

press 'n' to move onto next image
      'e' to exit
on resume: accurately indexes the saved images wrt no. of previously stored imgs
in images_true
'''

import cv2
import numpy as np
import argparse
import copy
import os, fnmatch

true_path = '_PATH_TO_CLASS_1_(POSITIVE)_'
train_path = '_PATH_TO_TRAINING_DATASET_'
refPt = []  #list to store top-left, bottom -right coordinates
imgIndex = 0
n_clk = -1
image = cv2.imread(os.path.join(train_path, '1(0).jpg'))
existing = 0

def saveImage(n_clk, roi):
    save_img = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)
    filename = str('%05d_true.JPG' %n_clk)
    cv2.imwrite(os.path.join(true_path,filename), save_img)
    print('file saved')
    
def draw_rect(evt,x,y,flags,param):
    global image, n_clk
    if evt == cv2.EVENT_LBUTTONDOWN:
        n_clk += existing + 1
        print('n_clk: %d' %n_clk)
        refPt = [(x,y)]
        refPt.append((x+38, y+28))
        #cv2.rectangle(image,(x,y),(x+220, y+80),(0,255,0),2) #3 is border thickness
        img_copy = copy.copy(image)
        roi = img_copy[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        cv2.imshow('roi ', roi)
        saveImage(n_clk, roi)
 
def fetch_img(imgIndex):
    #fetch images from path   
    #image = cv2.imread(os.path.join(train_path, '1(%d).jpg' %i))
    global image

    #===============================================================
    image = cv2.imread(os.path.join(train_path, '1(%d).jpg' %imgIndex))
    #===============================================================
    
    cv2.imshow('image', image)
    #clone = copy.copy(image)
    #cv2.imshow('image', image)  #show org image for drawing rects
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rect)

def init():
    while True:
        global imgIndex
        #image = cv2.imread(os.path.join(train_path, '1(%d).jpg' %(i+1)))
        #image = cv2.imread(os.path.join(train_path, '1(0).jpg'))
        ##fetch_img((i+1), image)
        #cv2.imshow('image', image)
        k = cv2.waitKey(0) & 0xFF
        if k == ord('n'):
            cv2.destroyAllWindows()
            imgIndex = imgIndex + 1
            fetch_img(imgIndex)
            print('next')
        elif k == ord('e'):
            print('exit')
            break
        else:
            fetch_img(imgIndex+1)

cv2.destroyAllWindows()

#def main():
    
if __name__ == "__main__":
    for image in os.listdir(true_path):
        if fnmatch.fnmatch(image, '*.jpg'):
            im = os.path.join(true_path, '1(%d).jpg' %(existing+1))
            #cv2.imread(cv2.UMat(im))
            #cv2.imshow('image', im)
            n_clk += 1
    print('total no. of imgs : ', existing)
    print('main')
    init()
