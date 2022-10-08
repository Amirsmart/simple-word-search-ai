import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
from os.path import isfile , join
from os import listdir
import os
import string
import skimage

# making cache directory 
if not os.path.exists('cache'):
    print("[*]  Creating cache directory ...")
    os.makedirs('cache')


# size of puzzle box from top-left window
bounding_box = {'top': 200, 'left': 270, 'width': 430, 'height': 550}
ROW = 15 # puzzle row length
COLUMN = 12 # puzzle column length

# using mss for capturing screen
sct = mss()

# compare target image with alphabet assets and return score
def compare(targetImage,mypath = 'assets'):
    assetFiles = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))] # load asset files
    assetFiles.sort() # sort asset files alphabetically
    targetLetter = '' # init target letter
    maxScore = 0 # maxScore of comapre results
    score = -1 # final score
    for p in assetFiles:
        p = str(p) + '.png'
        image_1 = cv2.imread(mypath + '/' + p, 0) # asset image
        image_2 = cv2.imread('cache' + '/' + targetImage, 0) # targetImage
        
        (H, W) = image_1.shape # get assetImage size
        # to resize and set the new width and height 
        image_2 = cv2.resize(image_2, (W, H))
        (score, diff) = skimage.metrics.structural_similarity(image_1, image_2, full=True) # get similarity score of asset and target image
        # find maximum score and set targetLetter
        if score >= maxScore:
            targetLetter = p
            maxScore = score

    if maxScore >= -1:
        return targetLetter[0]

def solver(pBox , word):
    pass

# print the puzzle box in right format
def print_puzzle_box(pBox):
    for i in range(ROW):
        for j in range(COLUMN):
            print(pBox[(i * COLUMN) + j] ,end=' ')
        print()

# take screenshot of puzzle box 
sct_img = sct.grab(bounding_box)
# convert screenshot to numpy array
img = np.array(sct_img)
# vertical distance between each alphabets in puzzle box
vertival_devider = 35
# hor distance between each alphabets in puzzle box
hor_devider = 35

puzzle_box = []

print("[*]  Scanning puzzle box ...")

# for loop on each alphabet of puzzle box
for i in range(ROW):
    for j in range(COLUMN):
        # cut the target alphabet
        alphabet = img[i*vertival_devider:(i+1)*vertival_devider , (j)*hor_devider:(j+1)*hor_devider]
        # write target alphabet as cache file
        cv2.imwrite('cache/%d%d.png'%(i,j),alphabet )
        # compare it with assets
        res = compare('%d%d.png'%(i,j))
        # add the alphabet to our box
        puzzle_box.append(res)
# print the puzzle box after scan        
print_puzzle_box(puzzle_box)   

# count number of input words
word_number = 1
# get words from user
while True:
    word = input("input word number%d or press q for quit: "%(word_number))
    # if target word == q exit from app
    if word == 'q':
        exit(0)
    # solve the puzzle
    result = solver(puzzle_box , word)
    word_number += 1