import cv2
import numpy as np
import math
from cvzone.HandTrackingModule import HandDetector

# 1. કેમેરા અને ડિટેક્ટર સેટઅપ (cvzone વડે)
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# 2. કલર્સ અને કેનવાસ સેટઅપ
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (0, 0, 0)]
color_index = 0

canvas = None
prev_x, prev_y = 0, 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    # હાથ ડિટેક્ટ કરો
    hands, frame = detector.findHands(frame, draw=False)

    # Top Color Palette
    cv2.rectangle(frame, (10, 10), (110, 60), (100, 100, 100), -1)
    cv2.putText(frame, "CLEAR", (25, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    for i, col in enumerate(colors):
        x1 = 130 + i * 90
        cv2.rectangle(frame, (x1, 10), (x1 + 80, 60), col, -1)
        if i == color_index:
            cv2.rectangle(frame, (x1, 10), (x1 + 80, 60), (255, 255, 255), 3)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]  # 21 Hand Landmarks

        # Index Finger (8) and Thumb (4) Coordinates
        ix, iy = lmList[8][0], lmList[8][1]
        tx, ty = lmList[4][0], lmList[4][1]

        # Pinch Distance (અંગૂઠા અને આંગળી વચ્ચેનું અંતર)
        distance = math.hypot(ix - tx, iy - ty)

        # Palette Selection
        if iy < 70:
            prev_x, prev_y = 0, 0
            if 10 <= ix <= 110:
                canvas = np.zeros_like(frame)
            else:
                for i in range(len(colors)):
                    x1 = 130 + i * 90
                    if x1 <= ix <= x1 + 80:
                        color_index = i

        # Drawing Mode (Pinch કરવા પર)
        elif distance < 40:
            cv2.circle(frame, (ix, iy), 8, colors[color_index], -1)

            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = ix, iy

            brush_thickness = 35 if color_index == 4 else 8
            cv2.line(canvas, (prev_x, prev_y), (ix, iy), colors[color_index], brush_thickness)
            prev_x, prev_y = ix, iy
        else:
            prev_x, prev_y = 0, 0

        cv2.circle(frame, (ix, iy), 6, (255, 255, 255), -1)

    # Frame and Canvas Merge
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, inv_mask = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY_INV)
    inv_mask = cv2.cvtColor(inv_mask, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, inv_mask)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.imshow("Air Sketch Pro", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()