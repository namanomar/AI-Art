from handTracker import *
import cv2
import mediapipe as mp
import numpy as np
import random

class ColorRect:
    def __init__(self, x, y, w, h, color, text='', alpha=0.5):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color, self.text, self.alpha = color, text, alpha
    
    def drawRect(self, img, text_color=(255, 255, 255), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8, thickness=2):
        bg_rec = img[self.y:self.y+self.h, self.x:self.x+self.w]
        white_rect = np.ones(bg_rec.shape, dtype=np.uint8) * np.array(self.color, dtype=np.uint8)
        img[self.y:self.y+self.h, self.x:self.x+self.w] = cv2.addWeighted(bg_rec, self.alpha, white_rect, 1-self.alpha, 1.0)
        text_size = cv2.getTextSize(self.text, fontFace, fontScale, thickness)[0]
        text_pos = (self.x + self.w // 2 - text_size[0] // 2, self.y + self.h // 2 + text_size[1] // 2)
        cv2.putText(img, self.text, text_pos, fontFace, fontScale, text_color, thickness)

    def isOver(self, x, y):
        return (self.x < x < self.x + self.w) and (self.y < y < self.y + self.h)

detector = HandTracker(detectionCon=0.8)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
canvas = np.zeros((720, 1280, 3), np.uint8)
px, py, color = 0, 0, (255, 0, 0)
brushSize, eraserSize = 5, 20

colorsBtn = ColorRect(200, 0, 100, 100, (120, 255, 0), 'Colors')
colors = [
    ColorRect(300, 0, 100, 100, (int(random.random() * 255), int(random.random() * 255), int(random.random() * 255))),
    ColorRect(400, 0, 100, 100, (0, 0, 255)),
    ColorRect(500, 0, 100, 100, (255, 0, 0)),
    ColorRect(600, 0, 100, 100, (0, 255, 0)),
    ColorRect(700, 0, 100, 100, (0, 255, 255)),
    ColorRect(800, 0, 100, 100, (0, 0, 0), "Eraser")
]
clear = ColorRect(900, 0, 100, 100, (100, 100, 100), "Clear")
pens = [ColorRect(1100, 50 + 100 * i, 100, 100, (50, 50, 50), str(penSize)) for i, penSize in enumerate(range(5, 25, 5))]
penBtn, boardBtn = ColorRect(1100, 0, 100, 50, color, 'Pen'), ColorRect(50, 0, 100, 100, (255, 255, 0), 'Board')
whiteBoard = ColorRect(50, 120, 1020, 580, (255, 255, 255), alpha=0.6)

coolingCounter, hideBoard, hideColors, hidePenSizes = 20, True, True, True

while True:
    if coolingCounter: coolingCounter -= 1
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.resize(cv2.flip(frame, 1), (1280, 720))
    detector.findHands(frame)
    positions, upFingers = detector.getPostion(frame, draw=False), detector.getUpFingers(frame)

    if upFingers:
        x, y = positions[8]
        if upFingers[1] and not whiteBoard.isOver(x, y):
            px, py = 0, 0
            if not hidePenSizes:
                for pen in pens:
                    if pen.isOver(x, y): brushSize = int(pen.text); pen.alpha = 0
                    else: pen.alpha = 0.5
            if not hideColors:
                for cb in colors:
                    if cb.isOver(x, y): color, cb.alpha = cb.color, 0
                    else: cb.alpha = 0.5
                clear.alpha = 0 if clear.isOver(x, y) else 0.5
                if clear.isOver(x, y): canvas = np.zeros((720, 1280, 3), np.uint8)
            if colorsBtn.isOver(x, y) and not coolingCounter:
                coolingCounter, colorsBtn.alpha = 10, 0
                hideColors, colorsBtn.text = not hideColors, 'Colors' if hideColors else 'Hide'
            else: colorsBtn.alpha = 0.5
            if penBtn.isOver(x, y) and not coolingCounter:
                coolingCounter, penBtn.alpha = 10, 0
                hidePenSizes, penBtn.text = not hidePenSizes, 'Pen' if hidePenSizes else 'Hide'
            else: penBtn.alpha = 0.5
            if boardBtn.isOver(x, y) and not coolingCounter:
                coolingCounter, boardBtn.alpha = 10, 0
                hideBoard, boardBtn.text = not hideBoard, 'Board' if hideBoard else 'Hide'
            else: boardBtn.alpha = 0.5

        elif upFingers[1] and not upFingers[2]:
            if whiteBoard.isOver(x, y) and not hideBoard:
                cv2.circle(frame, positions[8], brushSize, color, -1)
                if px == 0 and py == 0: px, py = positions[8]
                cv2.line(canvas, (px, py), positions[8], color, eraserSize if color == (0, 0, 0) else brushSize)
                px, py = positions[8]
        else:
            px, py = 0, 0

    colorsBtn.drawRect(frame); boardBtn.drawRect(frame)
    if not hideBoard:
        whiteBoard.drawRect(frame)
        canvasGray, imgInv = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY), None
        _, imgInv = cv2.threshold(canvasGray, 20, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        frame = cv2.bitwise_and(frame, imgInv)
        frame = cv2.bitwise_or(frame, canvas)

    if not hideColors:
        for c in colors: c.drawRect(frame)
        clear.drawRect(frame)

    penBtn.color = color; penBtn.drawRect(frame)
    if not hidePenSizes:
        for pen in pens: pen.drawRect(frame)

    cv2.imshow('video', frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
