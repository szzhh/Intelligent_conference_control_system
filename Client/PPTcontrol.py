import threading
import cv2
import os
import numpy as np
import math
import pyttsx3
import pyautogui
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True


def pptControl(cap, detector):
    n = 0
    i = 0
    while True:
        if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
                break
        # 1.import image
        success, img = cap.read()
        if not success:
            continue
        img = cv2.flip(img, 1)  # 翻转

        # 2.find hand landmarks
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=True)

        if len(lmList) != 0:
            fingers = detector.fingersUp()
            # if n < sum(fingers):
            n = sum(fingers)
            x1, y1, x2, y2, x3, y3 = lmList[4][1], lmList[4][2],lmList[8][1], lmList[8][2], lmList[12][1], lmList[12][2]
            dist = abs(x3 - x2)
            i += 1
            if i == 10:
                i %= 10
                print('Checking...........', n)

                if sum(fingers) == 0:
                    n == 0

                elif n == 5:
                    break

                elif fingers[1] and n == 1:
                    print('退出')
                    pyautogui.keyDown('esc')
                    #msg('exit# ', sock)

                elif fingers[4] and n == 1:
                    print('下一张')
                    #msg('next_page_of_ppt# ', sock)
                    pyautogui.keyDown('down')

                elif fingers[0] and n == 1:
                    print('上一张')
                    #msg('last_page_of_ppt# ', sock)
                    pyautogui.keyDown('up') 

                elif fingers[1] and fingers[2] and dist < 100 and n == 2:
                    print('播放')
                    pyautogui.hotkey('shift','f5')
                    #msg('parse# ', sock)

                else: 
                    print('Nothing happened')


        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)

# def msg(m, sock): 
#     t = threading.Thread(target=sock.send, kwargs={'msg': m})
#     t.start()
    
    