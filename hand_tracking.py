import cv2
import mediapipe as mp
import math
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
finger_count = 0

def calcdistance(x1, y1, x2, y2):
    print(x1, y1, x2, y2)
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

heimler_img = cv2.imread('heimler_1.jpg')

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_index, handLms in enumerate(result.multi_hand_landmarks):
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            landmarks = []
            finger_tips = []
            pip_joints = []
            up_fingers = []
            for idx, lm in enumerate(handLms.landmark):
                x_px = int(lm.x * w)
                y_px = int(lm.y * h)
                z = lm.z  # relative depth
                landmarks.append((idx, x_px, y_px, z))

                # visualize each landmark and its index
                cv2.circle(img, (x_px, y_px), 4, (0, 255, 0), -1)
                cv2.putText(img, str(idx), (x_px + 5, y_px + 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
            def determine_longer(dist1, dist2):
                if dist1>dist2:
                    up_fingers.append(dist1)
                
            finger_tips.append((landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]))
            pip_joints.append((landmarks[2], landmarks[6], landmarks[10], landmarks[14], landmarks[18]))
            wrist_base = landmarks[0]
            # use pinky MCP as a landmark for determining thumb position
            pinky_base = landmarks[17]

            determine_longer(calcdistance(finger_tips[0][0][1], finger_tips[0][0][2], pinky_base[1], pinky_base[2]), calcdistance(pip_joints[0][0][1], pip_joints[0][0][2], pinky_base[1], pinky_base[2]))
            for i in range(4):
                determine_longer(calcdistance(finger_tips[0][i+1][1], finger_tips[0][i+1][2], wrist_base[1], wrist_base[2]), calcdistance(pip_joints[0][i+1][1], pip_joints[0][i+1][2], wrist_base[1], wrist_base[2]))

            # print out and display num of fingers extended
            print(len(up_fingers))
            cv2.putText(img, str(len(up_fingers)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            
            # display image based on how many fingers are up
            cv2.imshow('Heimler\'s Reaction', heimler_img)
            match len(up_fingers):
                case 1:
                    heimler_img = cv2.imread('heimler_1.jpg')
                    break
                case 2:
                    heimler_img = cv2.imread('heimler_2.jpg')
                    break
                case 3:
                    heimler_img = cv2.imread('heimler_3.webp')
                    break
                case 4:
                    heimler_img = cv2.imread('heimler_4.webp')
                    break
                case 5:
                    heimler_img = cv2.imread('heimler5.webp')
                    break
                case _:
                    break

            cv2.imshow('Heimler\'s Reaction', heimler_img)
            # print out landmark metrics
            print(f"Hand {hand_index+1} landmarks:")
            for i in range(len(landmarks)):
                print(f"{i+1} {landmarks[i][1]}, {landmarks[i][2]}")

            # example: read a specific landmark (INDEX_FINGER_TIP)
            tip = handLms.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            tip_x, tip_y = int(tip.x * w), int(tip.y * h)
            print("Index finger tip (px):", tip_x, tip_y, "z:", tip.z)
    else:
        print("No Hand")

    cv2.imshow("Hand Tracker", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()