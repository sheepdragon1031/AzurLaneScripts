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
    scaled_pos = int(pos[0]), int(pos[1])
    print(scaled_pos)
    adb.run('shell input tap {} {}'.format(scaled_pos[0], scaled_pos[1]))
    return scaled_pos

def getView():
    screenshot.check_screenshot()
    im = screenshot.pull_screenshot()
    im = screenshot.Image2OpenCV(im)    
    return im
def getMap():
    template = cv2.imread('azurlane.jpg')
    # cv2.imshow("Templates", template)
    # cv2.waitKey()
    return template
def Combat(mode = 0):
    time.sleep(4)
    # getView()
    if mode == 0:
        pos, val = Moving.autoFing(getView(), 'bos.png')
        if val:
            Combat(1)
        else:
            Combat(2)
        
    if mode == 1:
        pos, val = Moving.autoFing(getMap(), 'bos.png')
        if val:
            print('發現Boss')
            tap_scale(pos)
            return (mode, 'Boss')
        else:
            Combat(2)
        
    else:
        if mode == 2:
            pos, val = Moving.autoFing(getMap(), 'A.png')
            if val:
                print('發現A')
                tap_scale(pos)
                return (mode, '小艇')
            else:
                Combat(3)
        else:
            if mode == 3:
                pos, val = Moving.autoFing(getMap(), 'C.png')
                if val:
                    print('發現C')
                    tap_scale(pos)
                    return (mode, '航母')
                else:
                    Combat(4)
            else:
                if mode == 4:
                    pos, val = Moving.autoFing(getMap(), 'B.png')
                    if val:
                        print('發現B')
                        tap_scale(pos)
                        return (mode, '戰艦')
                    else:
                        Combat(5)
                else:
                    print('壞掉了 目前找不到或是退出')
                    return (5, '???')
def Check( m = 3):
    
    Apos, Aval = Moving.autoFing(getView(), 'error.png')
    if(Aval):
        pos, val = Moving.autoFing(getView(), 'bos.png')
        mode , text = Combat(m)
        Check( m + 1)
    else:
        time.sleep(2)
        Bpos, Bval = Moving.autoFing(getMap(), 'ambush.png')
        if(Bval):
            Cpos, Cval = Moving.autoFing(getMap(), 'escape.png')
            if Cval:
                tap_scale(Cpos)
                print('幹你地雷!')
                print('重新Attack')
                Attack()
            else:
                time.sleep(2)
                Dpos, Dval = Moving.attack(getView(), 'attack.png')
                if Dval:
                    tap_scale(Dpos)
                    print('幹中標@_@')
                else:
                    print('重新Attack')
                    Attack()
        

def Attack():
    Combat(0)
    Check()
    time.sleep(2)
    ATpos, ATval = Moving.autoFing(getView(), 'attack.png')
    if(ATval):
        tap_scale(ATpos)
        print('載入戰鬥...')
        Sheep()
    else:
        print('被卡住? 再次點擊')
        Combat(1)
    time.sleep(1)
def Sheep():
    time.sleep(10)
    Ppos, Pval = Moving.autoFing(getView(), 'pause.png')
    print(Ppos, '遊戲中..')
    if (Pval):
        print('等待遊戲結束')
        time.sleep(30)
        Sheep()
    else:
        print('結束中...')
        endGame()
def endGame():
    print('===================')
    Apos, Aval = Moving.autoFing(getView(), 'endC.png')
    if Aval:
        print(Apos)
        tap_scale(Apos)
    Bpos, Bval = Moving.autoFing(getView(), 'endC.png')
    if Bval:
        print(Bpos)
        tap_scale(Bpos)
    Cpos, Cval = Moving.autoFing(getView(), 'accept.png')
    if Cval:
        print(Bpos)
        tap_scale(Cpos)
    print('退出關卡')
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
    for i in range(5):
        Attack()
    #     print(i)
    
    # Sheep()
    # endGame()
    # Check()
    # print(Apos)

if __name__ == '__main__':
    main()
