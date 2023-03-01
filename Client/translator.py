import cv2
import HandTrackingModule as htm
import os
import numpy as np
import math
import pyttsx3
import threading

FLAG = 0


def Translator(cap, detector):
    global FLAG
    strlst = ['0']
    n = 0
    i = 0
    while True:
        if cv2.waitKey(1) &0xFF == ord(' '):  #按空格键退出
                break
        # 1.import image
        success, img = cap.read()
        img = cv2.flip(img, 1)  # 翻转

        # 2.find hand landmarks
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=True)
        i += 1
        if i == 10: 
            i %= 10
            if len(lmList) != 0:
                fingers = detector.fingersUp()
                if n < sum(fingers):
                    n = sum(fingers)
                x1, y1, x2, y2, x3, y3 = lmList[4][1], lmList[4][2],lmList[8][1], lmList[8][2], lmList[12][1], lmList[12][2]
                dist = abs(x3 - x2)
                if sum(fingers) == 0:
                    n = 0
                    str = '0'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif n == 5 and not FLAG:
                    if strlst == ['0']: 
                        break
                    t = threading.Thread(target=say, kwargs={'result': result})
                    t.start()
                    strlst = ['0']
                    FLAG = 0
                    print(strlst == ['0'])

                # elif fingers[0] and n == 1:
                #     str = 'A'
                #     if strlst[-1] != str:
                #         strlst.append(str)

                elif fingers[1] and fingers[2] and fingers[3] and fingers[4] and n == 4:
                    str = ' '
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[1] and n == 1:
                    str = 'D'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[4] and n==1:
                    str = 'I'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[1] and fingers[2] and fingers[3] and n==3:
                    str = 'W'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[2] and fingers[3] and fingers[4] and n==3:
                    str = 'F'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[0] and fingers[1] and fingers[2] and n==3:
                    str = 'K'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[0] and fingers[1] and fingers[4] and n==3:
                    str = 'E'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[0] and fingers[1]  and x1<x3 and n==2:
                    str = 'L'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[0] and fingers[4]  and n==2:
                    str = 'Y'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[3] and fingers[4]  and n==2:
                    str = 'O'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[1] and fingers[2] and dist>100 and n==2:
                    str = 'V'
                    if strlst[-1] != str:
                        strlst.append(str)

                elif fingers[1] and fingers[2] and dist<100 and n==2:
                    str = 'U'
                    if strlst[-1] != str:
                        strlst.append(str)
                print(strlst)
        #print(strlst)
        # resultlst=[]
        # for i in range(1, len(strlst)):
        #     if strlst[i] == '0':
        #         resultlst.append(strlst[i-1])

        result = ''.join(strlst).replace('0', '')
        print(result)
        cv2.putText(img, result, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2)
        cv2.imshow("Image", img)
        # cv2.imshow("Canvas", imgCanvas)
        # cv2.imshow("Inv", imgInv)
        cv2.waitKey(1)

    

        
def say(result):
    global FLAG
    FLAG = 1
    engine = pyttsx3.init()
    engine.say(result)
    engine.runAndWait()
    FLAG = 0