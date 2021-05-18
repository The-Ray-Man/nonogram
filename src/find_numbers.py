import re
import cv2
import numpy as np
from collections import *
#######   training part    ############### 
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model =  cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE,responses)
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

############################# testing part  #########################
def get_numbers(path):
    im_real = cv2.imread(path)
    (y, x, _) = im_real.shape
    y1 = int(y/5)
    y2 = int(y/5*4)
    im = im_real[y1:y2]
    out = np.zeros(im.shape,np.uint8)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    result = list()
    for cnt in contours:
        if cv2.contourArea(cnt)>50 and cv2.contourArea(cnt) < 500:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if   h>28 and w<h:
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                string = str(int((results[0][0])))
                result.append([x,y,w,h,string])
    return result

def split_numbers(numbers):
    horizontal = list()
    vertical = list()
    distribution = defaultdict(list)
    offset = 0
    count = 0
    while count < len(numbers):
        for x,y,w,h,string in numbers:
            if offset <= x <= offset +50:
                distribution[offset].append([x,y,w,h,string])
                count += 1
        offset += 50
    last_value = 0
    vert = False
    for key, value in distribution.items():
        if len(value) < last_value // 2:
            vert = True
        last_value = len(value)
        if vert:
            vertical += value
        else:
            horizontal += value
    return vertical, horizontal

def get_speile(vertical, horizontal):
    horizontal_lines = defaultdict(list)
    while len(horizontal)>0:
        x,y,w,h,string = horizontal[0]
        horizontal_lines[y].append([x,y,w,h,string])
        horizontal.pop(0)
        for i,(x_,y_,w_,h_,string_) in enumerate(horizontal):
            if abs(y - y_) < 10:
                horizontal_lines[y].append([x_,y_,w_,h_,string_])
                horizontal.pop(i)

    vertical_lines = defaultdict(list)
    while len(vertical)>0:
        x,y,w,h,string = vertical[0]
        vertical_lines[x].append([x,y,w,h,string])
        vertical.pop(0)
        for i,(x_,y_,w_,h_,string_) in enumerate(vertical):
            if abs(x - x_) < 30:
                vertical_lines[x] = [[x_,y_,w_,h_,string_]] + vertical_lines[x]
                vertical.pop(i)
    return vertical_lines, horizontal_lines

def combine_results(vertical, horizontal):
    horizontal_info = defaultdict(list)
    for key, value in horizontal.items():
        last_x = 0
        horizontal_info[key] = list()
        for x,y,w,h,string in value:
            if abs(last_x - x) < 25:
                horizontal_info[key][-1] += string
            else:
                horizontal_info[key].append(string)
            last_x = x
    vertical_info = defaultdict(list)
    for key, value in vertical.items():
        last_y = 0
        vertical_info[key] = list()
        for x,y,w,h,string in value:
            if abs(last_y - y) < 25:
                vertical_info[key][-1] += string
            else:
                vertical_info[key].append(string)
            last_y = y
    return vertical_info, horizontal_info


def analize_image(device):
    numbers = get_numbers('pic.png')
    vertical_numbers, horizontal_numbers = split_numbers(numbers)
    vertical_speile, horizontal_speile = get_speile(vertical_numbers, horizontal_numbers)
    vertical, horizontal = combine_results(vertical_speile, horizontal_speile)
    vertical = OrderedDict(sorted(vertical.items()))
    horizontal = OrderedDict(sorted(horizontal.items()))
    vertical_cords = list(vertical.keys())
    horizontal_cords = list(horizontal.keys())
    return vertical_cords, horizontal_cords, vertical.values(), horizontal.values()

print(analize_image(None))
