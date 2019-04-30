#!/usr/bin/env python

'''
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
from perspective_transform import four_point_transform as transform

true_path = '_PATH_TO_STORE_IMAGES_'
train_path = '_PATH_TO_TRAIN_DATASET_'
refPt = []  #list to store top-left, bottom -right coordinates
imgIndex = 0
n_clk = -1
image = cv2.imread(os.path.join(train_path, '1(0).jpg'))
existing = 0
l_n_clk = 0
points = np.zeros(shape=(4,2))

def saveImage(n_clk, roi):
    save_img = cv2.resize(roi, (28, 28), interpolation = cv2.INTER_AREA)
    filename = str('%05d_true.JPG' %n_clk)
    cv2.imwrite(os.path.join(true_path,filename), save_img)
    print('file saved')
    
def draw_rect(evt,x,y,flags,param):
    global image, n_clk, l_n_clk, points
    if evt == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(image, (x, y), 1, (255, 0, 0), 3, 8)
        cv2.imshow('circle', image)
        n_clk += existing + 1
        l_n_clk += 1
        print('n_clk: %d' %n_clk)
        #refPt = [(x,y)]
        refPt.append((x,y))
        #cv2.rectangle(image,(x,y),(x+220, y+80),(0,255,0),2) #3 is border thickness

        if l_n_clk%4 == 0:
            cv2.destroyWindow('warped')
            img_copy = copy.copy(image)
            points = np.asarray(refPt, dtype="float32")
            print(points)
            #points.reshape((4,2))
            warped = transform(img_copy, points)
            #cv2.imshow('original', img_copy)
            cv2.imshow('warped', warped)
            cv2.waitKey(0)
            l_n_clk = 0
            #np.delete(points, [0,1,2,3], axis=1)   #why not working??
            '''
            img_copy = copy.copy(image)
            roi = img_copy[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
            cv2.imshow('roi ', roi)
            saveImage(n_clk, roi)
            '''
 
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
            n_clk += 1
    print('total no. of imgs : ', existing)
    print('main')
    init()
