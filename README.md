# some-opencv-stuff

Some experimentations using the opencv 4 library and python 3. The motivation arose when creating our own dataset and labelling them.

# annotations.py

Given the path to training images, this code creates dataset for positive and negative image dataset in two folders.

1. This code creates a bounding box from setting the mouse click as top-left corner coordinate. 
2. On each mouse click, the bounding box is saved with a serial number.
3. Numbering continues on session restart/ deleting the last image file.

# perspective_transform.py

This code is inspired from [Adrian Rosebrock's tutorial](https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/). Often when the image plane is not parallel to our viewing plane, the image appears skewed. This can make training a model more difficult. This code runs the perspective transform on the set of images.

The driver code invokes the function to run on multiple images until the user quits (hits 'e')

### Instructions:
1. mouse-click to draw bounding boxes
2. 'n' to hit next image
    Apparently, due to a bug in opencv, we must hit twice to move to the second image. ie. to move to the second image, hit 'n' twice. This occurs only for the first image.
