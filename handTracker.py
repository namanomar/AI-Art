import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        # Convert detection confidence to int between 0 and 100
        self.detectionCon = int(detectionCon * 100)
        self.trackCon = int(trackCon * 100)
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=detectionCon,  # Keep original float value for Hands()
            min_tracking_confidence=trackCon  # Keep original float value for Hands()
        )
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def getPostion(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList
    
    def getUpFingers(self, img):
        positions = self.getPostion(img, draw=False)
        upFingers = []
        if positions:
            # Thumb
            if positions[4][0] < positions[3][0]:
                upFingers.append(1)
            else:
                upFingers.append(0)
            
            # 4 Fingers
            for i in range(8, 21, 4):
                if positions[i][1] < positions[i-2][1]:
                    upFingers.append(1)
                else:
                    upFingers.append(0)
        return upFingers