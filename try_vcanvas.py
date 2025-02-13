import cv2
import numpy as np
import mediapipe as mp
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
canvas = np.zeros((480, 640, 3), dtype=np.uint8)  
overlay = np.zeros((480, 640, 3), dtype=np.uint8)  
cap = cv2.VideoCapture(0)
prev_positions = {"Right": None, "Left": None}
alpha = 0.2  
drawing_trails = {"Right": [], "Left": []}
bubble_trails = {"Right": [], "Left": []}
colors = {"Right": (0, 0, 500), "Left": (255, 0, 0)} 
def is_hand_closed(hand_landmarks):
    fingers = [
        hand_landmarks.landmark[tip].y > hand_landmarks.landmark[tip - 2].y
        for tip in [8, 12, 16, 20]
    ]
    return all(fingers)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    overlay.fill(0)
    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_label = results.multi_handedness[idx].classification[0].label
            if is_hand_closed(hand_landmarks):
                canvas.fill(0)
                drawing_trails[hand_label].clear()
                bubble_trails[hand_label].clear()
                continue
            index_tip = hand_landmarks.landmark[8]
            h, w, _ = frame.shape
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            if prev_positions[hand_label] is None:
                prev_positions[hand_label] = (index_x, index_y)
            else:
                px, py = prev_positions[hand_label]
                index_x = int(alpha * index_x + (1 - alpha) * px)
                index_y = int(alpha * index_y + (1 - alpha) * py)
                prev_positions[hand_label] = (index_x, index_y)
            fingers = [
                hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y
                for tip in [8, 12, 16, 20]
            ]
            drawing = fingers[0] and not any(fingers[1:])

            if drawing:
                drawing_trails[hand_label].append((index_x, index_y))
                bubble_trails[hand_label].append((index_x, index_y))
                if len(drawing_trails[hand_label]) > 1:
                    points = np.array(drawing_trails[hand_label], dtype=np.int32)
                    cv2.polylines(canvas, [points], False, colors[hand_label], 8)
                for i, (bx, by) in enumerate(bubble_trails[hand_label]):
                    alpha_bubble = max(0.1, 1.0 - i/15)
                    cv2.circle(overlay, (bx, by), 15 - i, (255, 255, 255), -1)
            else:
                drawing_trails[hand_label].clear()
                bubble_trails[hand_label].clear()

            if len(drawing_trails[hand_label]) > 50:
                drawing_trails[hand_label].pop(0)
            if len(bubble_trails[hand_label]) > 15:
                bubble_trails[hand_label].pop(0)
    frame = cv2.addWeighted(frame, 0.8, overlay, 0.4, 0)  
    frame = cv2.add(frame, canvas)  

    cv2.imshow("Enhanced Virtual Canvas", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()