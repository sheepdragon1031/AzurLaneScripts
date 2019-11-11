# -*- coding: utf-8 -*-
import cv2
import numpy as np
import imutils
import cv2
import argparse
from collections import Counter

def findPic(img_bg_path, img_slider_path):
    """
    找出图像中最佳匹配位置
    :param img_bg_path: 滑块背景图本地路径
    :param img_slider_path: 滑块图片本地路径
    :return: 返回最差匹配、最佳匹配对应的x坐标
    """

    # 读取滑块背景图片，参数是图片路径，OpenCV默认使用BGR模式
    # cv.imread()是 image read的简写
    # img_bg 是一个numpy库ndarray数组对象
    img_bg = img_bg_path

    # 对滑块背景图片进行处理，由BGR模式转为gray模式（即灰度模式，也就是黑白图片）
    # 为什么要处理？ BGR模式（彩色图片）的数据比黑白图片的数据大，处理后可以加快算法的计算
    # BGR模式：常见的是RGB模式
    # R代表红，red; G代表绿，green;  B代表蓝，blue。
    # RGB模式就是，色彩数据模式，R在高位，G在中间，B在低位。BGR正好相反。
    # 如红色：RGB模式是(255,0,0)，BGR模式是(0,0,255)
    img_bg_gray = cv2.cvtColor(img_bg, cv2.COLOR_BGR2GRAY)

    # 读取滑块，参数1是图片路径，参数2是使用灰度模式
    image_path = 'resource/image/'
    img_slider_gray = cv2.imread(image_path + img_slider_path, 0)

    # 在滑块背景图中匹配滑块。参数cv.TM_CCOEFF_NORMED是opencv中的一种算法
    res = cv2.matchTemplate(img_bg_gray, img_slider_gray, cv2.TM_CCOEFF_NORMED)

    print('#' * 50)
    print(type(res))  # 打印：<class 'numpy.ndarray'>
    print(res)
    # 打印：一个二维的ndarray数组
    # [[0.05604218  0.05557462  0.06844381... - 0.1784117 - 0.1811338 - 0.18415523]
    #  [0.06151756  0.04408009  0.07010461... - 0.18493137 - 0.18440475 - 0.1843424]
    # [0.0643926    0.06221284  0.0719175... - 0.18742703 - 0.18535161 - 0.1823346]
    # ...
    # [-0.07755355 - 0.08177952 - 0.08642308... - 0.16476074 - 0.16210903 - 0.15467581]
    # [-0.06975575 - 0.07566144 - 0.07783117... - 0.1412715 - 0.15145643 - 0.14800543]
    # [-0.08476129 - 0.08415948 - 0.0949327... - 0.1371379 - 0.14271489 - 0.14166716]]

    print('#' * 50)

    # cv2.minMaxLoc() 从ndarray数组中找到最小值、最大值及他们的坐标
    value = cv2.minMaxLoc(res)
    # 得到的value，如：(-0.1653602570295334, 0.6102921366691589, (144, 1), (141, 56))

    print(value, "#" * 30)

    # 获取x坐标，如上面的144、141
    print(value[2:][0][0] ,'???', value[2:][1][0])
    pos = (value[2:][0][0], value[2:][1][0])
    return pos, value


def template_matching(screenshot, template):
   
    image_path = 'resource/image/'
    template = cv2.imread(image_path + template)
    
    # load the image image, convert it to grayscale, and detect edges
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    # cv2.imshow("Template", template)
    # cv2.waitKey()
    
    # loop over the images to find the template in
    

    # for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # imagePath = screenshot.copy()
        # load the image, convert it to grayscale, and initialize the
        # bookkeeping variable to keep track of the matched region
    # image = cv2.imread(imagePath)
   
    image = screenshot.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

       
        # if we have found a new maximum correlation value, then ipdate
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

        # unpack the bookkeeping varaible and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # draw a bounding box around the detected result and display the image
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    pos = ( (startX + endX) / 2, (startY + endY) / 2)
    # cv2.imshow("Image", image)
    # cv2.imwrite("Image.jpg", image)
    # cv2.waitKey()
        
    return pos, maxLoc

def autoFing(screenshot, template):
    Dlist = []
    image_path = 'resource/image/'
    template = cv2.imread(image_path + template)
    
    # load the image image, convert it to grayscale, and detect edges
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    
    # loop over the images to find the template in
    

    # for imagePath in glob.glob(args["images"] + "/*.jpg"):
    # imagePath = screenshot.copy()
        # load the image, convert it to grayscale, and initialize the
        # bookkeeping variable to keep track of the matched region
    # image = cv2.imread(imagePath)
   
    image = screenshot.copy()
    (IH, IW) = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found = None

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.2, 20)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

       
        # if we have found a new maximum correlation value, then ipdate
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

        # unpack the bookkeeping varaible and compute the (x, y) coordinates
        # of the bounding box based on the resized ratio
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
        # print(maxVal > (tH * tW) * (IH/tH) * (IW/tW) * 10)
        if maxVal > (tH * tW) * (IH/tH) * (IW/tW) * 10:
            Dlist.append((startX, startY, endX, endY))

        # draw a bounding box around the detected result and display the image
    # cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    # pos = ( (startX + endX) / 2, (startY + endY) / 2)
    
    Dresult = Counter(Dlist)
    Dget = Dresult.most_common()
    
    for Dout in Dget:
        xy = Dout[0]
        if Dout[1] > 1:
            cv2.rectangle(image, (xy[0] , xy[1]), (xy[2] , xy[3]), (0, 255, 0), 2)
        elif len(Dget) == 1:
            cv2.rectangle(image, (xy[0] , xy[1]), (xy[2] , xy[3]), (0, 255, 0), 2)
   
    if( len(Dget) > 0):
        one = Dget[0][0]
    else:
        return False, False
    # cv2.imshow("Image", image)
    # cv2.waitKey()
    return ( (one[0] + one[2]) * 0.5, (one[1] + one[3]) * 0.5), maxLoc
    
    

def find_enemy(screenshot):
    pos, val = template_matching(screenshot, 'boss.png')
    # if val > 0.2:
    #     pos, val = template_matching(screenshot, 'mid-air.png')
    #     if val > 0.06:
    #         pos, val = template_matching(screenshot, 'mid-defense.png')
    #         if val > 0.15:
    #             pos, val = template_matching(screenshot, 'mid-main.png')
    if val > 0.2:
        pos, val = template_matching(screenshot, 'easy.png')
        if val > 0.06:
            pos, val = template_matching(screenshot, 'nomal.png')
            if val > 0.15:
                pos, val = template_matching(screenshot, 'hard.png')
    return pos


def attack(screenshot):
    pos, val = template_matching(screenshot, 'attack.png')
    return pos, val


def escape(screenshot):
    return template_matching(screenshot, 'escape.png')


def ambush(screenshot):
    pos, val = template_matching(screenshot, 'ambush.png')
    return pos, val


def finished(screenshot):
    pos, val = template_matching(screenshot, 'finished.png')
    return pos, val


def accept(screenshot):
    pos, val = template_matching(screenshot, 'accept.png')
    return pos, val


def find_stage(screenshot, stage):
    pos, val = template_matching(screenshot, stage + '.png')
    #pos = (pos[0] - 88, pos[1])
    return pos, val


def go(screenshot):
    return template_matching(screenshot, 'go.png')
