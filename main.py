import numpy as np
import cv2
from mss import mss
from PIL import Image
import time
from os.path import isfile , join
from os import listdir
import string
import skimage


words = [
'O','N','O','I','T','A','L','F','E','D','R','P',
'U','R','O','T','A','C','I','L','P','P','A','D',
'T','L','C','O','N','V','E','Y','A','N','C','E',
'F','S','C','H','E','M','A','H','E','S','D','A',
'C','T','R','T','D','U','L','L','Y','S','I','R',
'A','I','E','L','S','T','P','O','B','E','S','E',
'B','T','U','L','I','A','P','Y','N','E','L','F',
'B','E','M','I','S','T','E','R','T','I','L','H',
'Y','L','S','U','O','I','C','I','P','S','U','S',
'P','B','J','D','V','O','I','C','P','H','F','L',
'T','A','N','K','E','N','R','H','A','N','S','A',
'O','T','N','E','L','E','P','P','A','R','N','B',
'L','L','D','E','M','R','A','H','C','L','U','I',
'F','L','A','M','E','N','C','O','U','R','E','D',
'C','U','H','A','N','D','I','W','O','R','K','F'
]


bounding_box = {'top': 200, 'left': 270, 'width': 430, 'height': 550}
ROW = 15
COLUMN = 12

sct = mss()

def compare(targetImage,mypath = 'assets'):
    cachFiles = [f[:-4] for f in listdir(mypath) if isfile(join(mypath, f))]

    cachFiles.sort()
    res = ''
    mx = 0
    score = -1
    for p in cachFiles:
        p = str(p) + '.png'
        image_1 = cv2.imread(mypath + '/' + p, 0)
        image_2 = cv2.imread('cache' + '/' + targetImage, 0)
        
        (H, W) = image_1.shape
        # to resize and set the new width and height 
        image_2 = cv2.resize(image_2, (W, H))
        (score, diff) = skimage.metrics.structural_similarity(image_1, image_2, full=True)
        ccc= score
        #print(p , mx , ccc , p2,'\n--------')
        if ccc >= mx:
            res = p
            mx = ccc

    if score >= -1:
        return res[0]
    else:
        pass
        print(score , res[0])


while True:

    sct_img = sct.grab(bounding_box)
    img = np.array(sct_img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w , _ = img.shape
    vertival_devider = 35
    vertival2_devider = 35
    
    hor_devider = 35
    hor2_devider = 35
    
    data = []
    for i in range(ROW):
        for j in range(COLUMN):
            word = img[i*vertival2_devider:(i*vertival2_devider)+vertival_devider , (j)*hor2_devider:((j)*hor2_devider)+hor_devider]
            cv2.imwrite('cache/%d%d.png'%(i,j),word )
            res = compare('%d%d.png'%(i,j))
            pointer = (i * 12) + j
            if res == None:
                res = '-'
            if res != words[pointer]:
                print(res + '-' + words[pointer] , end=' ')
            else:
                print(res  , end=' ')
                
        print()
    break
    cv2.imshow('screen' , img)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.des
    
    time.sleep(1)