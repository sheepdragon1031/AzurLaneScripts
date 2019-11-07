# -*- coding: utf-8 -*-
import cv2
import numpy as np
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
    image = screenshot.copy()
    template = cv2.imread(image_path + template)

    # Resize images
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    template = cv2.resize(template, (0,0), fx=0.5, fy=0.5)
    
    # Convert to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    # Find template
    result = cv2.matchTemplate(imageGray,templateGray, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    h,w = templateGray.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(image,top_left, bottom_right,(0,0,255),4)
    pos = (top_left[0] + w, top_left[1] + h)
    # Show result
    cv2.imshow("Result", image)
    cv2.imshow("Template", template) 
    cv2.moveWindow("Template", 10, 50)
    cv2.moveWindow("Result", 150, 50)

    print(top_left)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    # mid_air = cv2.imread(image_path + template, 0)
    # h, w = mid_air.shape[:2]
    # methods = ['cv2.TM_CCORR_NORMED']
    # # ,'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'
    # img_Gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('meth', mid_air)
    # for meth in methods:
    #     method = eval(meth)
    #     img = img_Gray.copy()
    #     result = cv2.matchTemplate(img, mid_air, method)
        
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #     strmin_val = str(min_val)
    #     print("匹配度：" + strmin_val)
    #     print( (min_loc[0] * 2 + w)  , (min_loc[1] * 2 + h) )
    #     cv2.rectangle(screenshot, min_loc, (min_loc[0] + w, min_loc[1] + h), (0, 0, 255))
        
    #     pos = (min_loc[0] + w / 2, min_loc[1] + h / 2)
        
    cv2.imshow('meth', screenshot)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # threshold = 0.8
    # loc = np.where( result >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

   
    # cv2.imshow("mid_air", mid_air)
    
    return pos, min_val


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
