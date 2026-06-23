import cv2
import time

from vision.hand_tracker import HandTracker


def main():
    cap = cv2.VideoCapture(0)

    tracker = HandTracker()

    previous_time = 0

    while True:
        success, frame = cap.read()

        if not success:
            print("Could not access webcam")
            break

        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame)

        landmarks = tracker.get_landmarks(frame)

        if landmarks:
            index_tip = landmarks[8]

            cv2.circle(
                frame,
                (index_tip["x"], index_tip["y"]),
                10,
                (255, 0, 255),
                cv2.FILLED,
            )

            print(
                "Index Tip:",
                index_tip["x"],
                index_tip["y"]
            )

        current_time = time.time()

        fps = 1 / (current_time - previous_time) if previous_time else 0
        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Frame & Solve", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()