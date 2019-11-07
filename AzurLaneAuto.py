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


def tap_scale(pos, scale):
    scaled_pos = int(pos[0] * scale[0]), int(pos[1] * scale[1])
    print(scaled_pos)
    adb.run('shell input tap {} {}'.format(scaled_pos[0], scaled_pos[1]))
    return scaled_pos


def main():
    screenshot.check_screenshot()
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)
    x, y = adb.get_size()
    if x < y:
        x, y = y, x
    scale = (x / 1280, y / 640)
    # pos, val = Moving.find_stage(im, 'RedEX')
    
    # pos, val = Moving.find_stage(im, '3-4')
    # print('pos val', pos, val)
    # tap_scale(pos, scale)
    
    # im = screenshot.pull_screenshot()
    # im = screenshot.Image2OpenCV(im)
    pos, val = Moving.go(im)
    tap_scale(pos, scale)
    # im = screenshot.pull_screenshot()
    # im = screenshot.Image2OpenCV(im)
    # pos, val = Moving.go(im)
    # tap_scale(pos, scale)
    # time.sleep(4)

    # while True:
    #     im = screenshot.pull_screenshot()
    #     im = screenshot.Image2OpenCV(im)
    #     pos = Moving.find_enemy(im)
    #     posx = pos
    #     tap_scale(pos, scale)
    #     time.sleep(4.5)
    #     im = screenshot.pull_screenshot()
    #     im = screenshot.Image2OpenCV(im)
    #     pos, val = Moving.attack(im)
    #     if val < 0.05:
    #         print('出擊！')
    #         tap_scale(pos, scale)
    #     else:
    #         pos, val = Moving.ambush(im)
    #         if val < 0.1:
    #             print('遭遇伏擊！規避')
    #             pos, val = Moving.escape(im)
    #             tap_scale(pos, scale)
    #         else:
    #             print('遭遇空襲！繼續進行')
    #             tap_scale(posx, scale)
    #         # 继续
    #         tap_scale(posx, scale)
    #         time.sleep(2.5)
    #         im = screenshot.pull_screenshot()
    #         im = screenshot.Image2OpenCV(im)
    #         pos, val = Moving.attack(im)
    #         # 出击
    #         tap_scale(pos, scale)
    #     val = 1
    #     while val > 0.06:
    #         print("判斷是否戰鬥結束，如果暫時進入戰斗狀態，請手動進入戰鬥")
    #         time.sleep(1)
    #         im = screenshot.pull_screenshot()
    #         im = screenshot.Image2OpenCV(im)
    #         pos, val = Moving.finished(im)
    #     tap_scale(pos, scale)
    #     time.sleep(0.5)
    #     tap_scale((500, 300), scale)
    #     time.sleep(1.5)
    #     im = screenshot.pull_screenshot()
    #     im = screenshot.Image2OpenCV(im)
    #     pos, val = Moving.accept(im)
    #     tap_scale(pos, scale)
    #     time.sleep(4.5)
    #     im = screenshot.pull_screenshot()
    #     im = screenshot.Image2OpenCV(im)
    #     pos, val = Moving.find_stage(im, '3-4')
    #     if val < 0.06:
    #         tap_scale(pos, scale)
    #         im = screenshot.pull_screenshot()
    #         im = screenshot.Image2OpenCV(im)
    #         pos, val = Moving.go(im)
    #         tap_scale(pos, scale)
    #         im = screenshot.pull_screenshot()
    #         im = screenshot.Image2OpenCV(im)
    #         pos, val = Moving.go(im)
    #         tap_scale(pos, scale)
    #         time.sleep(4)


if __name__ == '__main__':
    main()
