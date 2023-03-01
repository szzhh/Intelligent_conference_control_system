import cv2
import mediapipe as mp
import threading
# import multiprocessing
import time
from OurDemo.Server.HandTrackingModule import Camera

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

camera = Camera(0)
camera.open()
# For webcam input:
#cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    # model_complexity=0,
    0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.1) as hands:
  while True:
    time_s = time.time()
    success, image = camera.read()
    time_e = time.time()
    period_1 = time_e - time_s
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue
    # image = cv2.resize(image, (600, 400))
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    time_s = time.time()
    results = hands.process(image)
    time_e = time.time()
    period_2 = time_e - time_s

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            # mp_hands.HAND_CONNECTIONS,
            # mp_drawing_styles.get_default_hand_landmarks_style(),
            # mp_drawing_styles.get_default_hand_connections_style())
            )
   # flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(1) & 0xFF ==ord(' ') :
      break
    print('Fetching image: {}  Processing image: {}'.format(period_1, period_2))
camera.rls()
