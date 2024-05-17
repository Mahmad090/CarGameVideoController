import cv2
import time
import HandTrackingModule as htm
import pyautogui
import subprocess
import multiprocessing

def run_script():
    script_to_run = 'car_game.py'

    try:
        subprocess.run(['python', script_to_run])
    except Exception as e:
        print("An error occurred while running the external script:", str(e))

if __name__ == "__main__":
    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    pTime = 0

    detector = htm.handDetector(detectionCon=1)
    totalFingers = None
    tipIds = [4, 8, 12, 16, 20]
    move = True
    running = True

    script_process = multiprocessing.Process(target=run_script)
    script_process.start()

    while running:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            fingers = []

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            if totalFingers == 1 and move:
                pyautogui.press('left')
                pyautogui.keyUp('left')
                move = False
            elif totalFingers == 2 and move:
                pyautogui.press('right')
                pyautogui.keyUp('right')
                move = False
            elif totalFingers == 0:
                move = True

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.imshow("Image", img)
        cv2.waitKey(1)
