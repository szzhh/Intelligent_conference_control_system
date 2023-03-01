import cv2
import HandTrackingModule as htm
from HandTrackingModule import Camera
import time
import threading
import numpy as np

def CountFinger(cap, detector):
    time_s = time.time()
    ans = np.array([0, 0, 0, 0, 0, 0])
    fingers_flags = [0] * 20
    i = 0
    while True:
        success, img = cap.read()
        if not success:
            continue
        
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=False)
        
        fingersUp = detector.fingersUp()
        i = (i + 1) % 20
        fingers_flags[i] = sum(fingersUp)
        if sum(fingers_flags) >= 75: 
            break

        img = cv2.flip(img, 1)
        pointList = [4, 8, 12, 16, 20]
        if len(lmList) != 0:
            countList = []
            # 大拇指
            if lmList[4][1] > lmList[3][1]:
                countList.append(1)
            else:
                countList.append(0)
            # 余下四个手指
            for i in range(1, 5):
                if lmList[pointList[i]][2] < lmList[pointList[i] - 2][2]:
                    countList.append(1)
                else:
                    countList.append(0)
            # print(countList)

            count = countList.count(1)  # 对列表中含有的1计数
            # HandImage = cv2.imread('/home/oneran/Handpose/OurDemo/FingerImg/{}.jpg'.format(count))
            # if type(HandImage) != NoneType:
            #     HandImage = cv2.resize(HandImage, (150, 200))
            #     h, w, c = HandImage.shape
            #     img[0:h, 0:w] = HandImage
            #     cv2.putText(img, f'{int(count)}', (15, 400), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 255), 10)
    
            cv2.putText(img, f'FingerNum: {int(count)}', (200, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            ans[int(count)] += 1

        cTime = time.time()
        pTime = cTime
        lasting_time = time.time() - time_s
        if lasting_time >= 2: 
            break
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
    return np.argmax(ans)