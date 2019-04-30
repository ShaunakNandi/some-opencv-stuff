import numpy as np
import cv2

'''
order_points takes pts list of four coordinates
'''
def order_points(pts):
    #(x, y) for top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4,2), dtype="float32")

    s = pts.sum(axis=1) #axis=1 indicates row-wise
    rect[0] = pts[np.argmin(s)] #top-left
    rect[2] = pts[np.argmax(s)] #bottom-left

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  #top-right
    rect[3] = pts[np.argmax(diff)]  #bottom-right

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    #find max width between bottom (x,y) or top (x,y)
    widthT = np.sqrt(((tr[0]-tl[0])**2) + ((tr[1]-tl[1])**2))
    widthB = np.sqrt(((br[0]-bl[0])**2) + ((br[1]-bl[1])**2))
    maxWidth = max(int(widthT), int(widthB))
    #lly for height
    heightT = np.sqrt(((tr[0]-br[0])**2) + ((tr[1]-br[1])**2))
    heightB = np.sqrt(((tl[0]-bl[0])**2) + ((tl[1]-bl[1])**2))
    maxHeight = max(int(heightT), int(heightB))
    #new image shape = (maxHeight, maxWidth)

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    #compute and then apply the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

    
