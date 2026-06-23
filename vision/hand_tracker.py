import cv2
import mediapipe as mp


class HandTracker:
    def __init__(
        self,
        mode=False,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.7,
    ):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence,
        )

        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame, draw=True):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:

                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return frame

    def get_landmarks(self, frame, hand_index=0):
        landmarks = []

        if self.results.multi_hand_landmarks:
            selected_hand = self.results.multi_hand_landmarks[hand_index]

            h, w, _ = frame.shape

            for idx, lm in enumerate(selected_hand.landmark):
                cx = int(lm.x * w)
                cy = int(lm.y * h)

                landmarks.append({
                    "id": idx,
                    "x": cx,
                    "y": cy
                })

        return landmarks