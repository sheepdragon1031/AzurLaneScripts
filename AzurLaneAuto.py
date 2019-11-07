# -*- coding: utf-8 -*-
import cv2
import os
import random
import sys
import time
from PIL import Image
import Moving
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

if sys.version_info.major != 3:
    print('請使用python3.x版本')
    exit(1)
try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
except Exception as ex:
    print(ex)
    print('請將腳本放在項目根目錄中運行')
    print('請檢查項目根目錄中的 common 文件夾是否存在')
    exit(1)

adb = auto_adb()
adb.test_device()


def tap_scale(pos):
    scaled_pos = int(pos[0] ), int(pos[1])
    print(scaled_pos)
    adb.run('shell input tap {} {}'.format(scaled_pos[0], scaled_pos[1]))
    return scaled_pos

def getView():
    screenshot.check_screenshot()
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)    
    return im

def main():
  
    x, y = adb.get_size()
    if x < y:
        x, y = y, x
    
    # pos, val = Moving.find_stage(im, 'RedEX')
    
    # pos, val = Moving.find_stage(getView(), '3-4')
    # tap_scale(pos)
    

    # pos, val = Moving.go(getView())
    # tap_scale(pos)
    

   
    # pos, val = Moving.go(getView())
    # tap_scale(pos)
    # time.sleep(4)

    

if __name__ == '__main__':
    main()
