import sys 
from HandTrackingModule import *
from FingerCounter import *
from AiVirtualPainter import *
# from ClientCommunicationModule import *
from PPTcontrol import *
import os 
import time
from translator import *


detector = HandDetector()
cap = Camera(0)
cap.open()
#client_sock = ClientSocket('A4:C3:F0:BE:4E:24')
client_sock = None

#* 刚开始进入 首先选择是哪个模块 这里要自己选择一下
#* 1. 电脑综合控制
#* 2. 手语识别
#* 3. 画板绘制
n=0
while True:
    finger_num = CountFinger(cap, detector)
    print('Choose function: {}'.format(finger_num))
    #* 电脑综合控制
    if finger_num == 1:
        n=0
        VirtualPainter(cap, detector)
    
    elif finger_num == 2: 
        n=0
        MouseControler(cap, detector)
    
    elif finger_num == 3:
        n=0
        pptControl(cap, detector)
    
    elif finger_num == 4:
        n=0
        Translator(cap, detector)

    elif finger_num == 5:
        n=n+1
        print(n)
    if n > 1:
        break
        