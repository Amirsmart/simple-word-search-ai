import numpy as np
import cv2
from mss import mss
from os.path import isfile , join
from os import listdir
import os
import skimage
from colored import fg, bg, attr

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

def sub_solver(x,y,word,pBox,move,pointer=1,result=[]):
    # table of avaiable moves
    moves = {
        'r':[0,1],
        'l':[0,-1],
        'u':[1,0],
        'd':[-1,0],
        'ru':[1,1],
        'rd':[-1,1],
        'lu':[1,-1],
        'ld':[-1,-1]
    }
    # this flag is for checking the final result
    flag = False
    # if the pointer is bigger than target word return flag
    if pointer >= len(word):
        return flag
    
    # get target direction and convert it to 2d
    i , j = moves[move]
    # get previous alphabet location 
    xy1 = (x * COLUMN) + y
    # get current alphabet 2d location
    x2 = x + i
    y2 = y + j
    # convert 2d location to 1d location
    xy2 = (x2 * COLUMN) + y2
    # check if 1d location is in puzzle box
    cond1 = xy2 > 0 and xy2 < len(pBox)
    # check if y2 is in COLUMN range
    cond2 = y2 >=0 and y2 < COLUMN
    # check if x2 is in ROW range
    cond3 = x2 >= 0 and x2 < ROW
    # check if current location is not equal with previous location
    cond4 = xy1 != xy2 
    # check if all conditions is True
    if  cond1 and cond2 and cond3 and cond4:
        # check if current alphabet is equal with previous alphabet
        if pBox[xy2] == word[pointer]:
            # if it is last one return the answer
            if pointer + 1 == len(word):
                return [*result,xy2]
            # check if we can get the answer
            flag = flag or sub_solver(x2,y2,word,pBox,move,pointer+1,[*result,xy2])
            

    return flag
        
def solver(pBox , word):
    # check all cells
    for i in range(ROW):
        for j in range(COLUMN):
            # if starting alphabet of word is equal with cell alphabet
            if word[0] == pBox[(i * COLUMN) + j]:
                # all avaiables directions
                directions = ['r','l','u','d','ru','rd',
                    'lu','ld']
                # check if we can get the answer from all dircetions
                for direction in directions:
                    # check the answer
                    result = sub_solver(i,j , word,pBox,direction)
                    if result :
                        result =[(i * COLUMN) + j , *result]
                        # print the answer in another color
                        print_puzzle_box(pBox,result)
                        pass
    

# print the puzzle box in right format
def print_puzzle_box(pBox , select=[]):
    for i in range(ROW):
        for j in range(COLUMN):
            xy = (i * COLUMN) + j
            if xy in select:
                print(f"{fg(1)}{attr(5)}{pBox[xy]}{attr('reset')}" ,end=' ')
            else:
                print(pBox[xy] ,end=' ')
                
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
    # convert input to uppercase
    word = word.upper()
    # if target word == q exit from app
    if word == 'q':
        exit(0)
    # solve the puzzle
    result = solver(puzzle_box , word)
    word_number += 1