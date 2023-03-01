import cv2
import HandTrackingModule as htm
from HandTrackingModule import Camera
import os
import numpy as np
import threading
import pyautogui
pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

def VirtualPainter(cap, detector):
    folderPath = os.path.split(os.path.realpath(__file__))[0]+'/PainterImg/'
    mylist = os.listdir(folderPath)
    overlayList = []
    for imPath in mylist:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    header = overlayList[0]
    color = [255, 0, 0]
    brushThickness = 15
    eraserThickness = 100    
    xp, yp = 0, 0
    #* 需要重新制作画板
    #* new canvas
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板
    # imgCanvas = np.zeros((500, 800, 3), np.uint8)  # 新建一个画板
    fingers_flags = [0] * 20
    i = 0
    while True:
        if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
                break
        # 1.import image
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 翻转
        if not success:
            continue

        # 2.find hand landmarks
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=True)
        #* 判断是否退出
        fingersUp = detector.fingersUp()
        i = (i + 1) % 10
        fingers_flags[i] = sum(fingersUp)
        if sum(fingers_flags) >= 40: 
            break
            

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            # 4. If Selection Mode – Two finger are up
            if fingers[1] and fingers[2]:
                if y1 < 153:
                    if 0 < x1 < 320:
                        header = overlayList[0]
                        color = [50, 128, 250]
                    elif 320 < x1 < 640:
                        header = overlayList[1]
                        color = [0, 0, 255]
                    elif 640 < x1 < 960:
                        header = overlayList[2]
                        color = [0, 255, 0]
                    elif 960 < x1 < 1280:
                        header = overlayList[3]
                        color = [0, 0, 0]
            img[0:1280][0:153] = header

            # 5. If Drawing Mode – Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if color == [0, 0, 0]:
                    cv2.line(img, (xp, yp), (x1, y1), color, eraserThickness)  # ??
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), color, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), color, brushThickness)   # ??
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), color, brushThickness)
            
            if sum(fingers_flags) <= 5: 
                imgCanvas = np.zeros((720, 1280, 3), np.uint8)


            xp, yp = x1, y1
        # 实时显示画笔轨迹的实现
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)
        img[0:1280][0:153] = header

        cv2.imshow("Image", img)
        cv2.waitKey(1)

def MouseControler(cap, detector):
    color = [255, 0, 0] 
    xp, yp = 0, 0
    #* 需要重新制作画板
    #* new canvas
    imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # 新建一个画板
    # imgCanvas = np.zeros((500, 800, 3), np.uint8)  # 新建一个画板
    fingers_flags = [0] * 10
    i = 0
    size_x, size_y = pyautogui.size()
    while True:
        if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
                break
        # 1.import image
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 翻转
        if not success:
            continue

        # 2.find hand landmarks
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=True)
        #* 判断是否退出
        fingersUp = detector.fingersUp()
        i = (i + 1) % 10
        fingers_flags[i] = sum(fingersUp)
        if sum(fingers_flags) >= 40: 
            break
            

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            # 3. Check which fingers are up
            fingers = detector.fingersUp()

            # 5. If Drawing Mode – Index finger is up
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

            xp, yp = x1, y1
            xp, yp = xp*size_x/1280, yp*size_y/720
            pyautogui.moveTo(xp,yp)
            if fingers[1] and fingers[0]:
                pyautogui.click()
        # 实时显示画笔轨迹的实现
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        cv2.imshow("Image", img)
        cv2.waitKey(1)