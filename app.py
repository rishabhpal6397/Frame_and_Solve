import cv2
import time
from vision.hand_tracker import HandTracker
from puzzle.generator import PuzzleGenerator
from puzzle.puzzle_game import PuzzleGame

def draw_status(frame, text, color=(255, 255, 255)):
    cv2.putText(
        frame,
        text,
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    previous_time = 0
    capture_cooldown = 2
    last_capture_time = 0
    captured_image = None

    while True:
        success, frame = cap.read()

        if not success:
            print("Could not access webcam")
            break

        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame)

        # landmarks = tracker.get_landmarks(frame)

        hands = tracker.get_all_hands(frame)
        status = "Show both hands"
        status_color = (0, 0, 255)

        if len(hands) == 1:
            status = "Need 2 hands"
            status_color = (0, 165, 255)

        # if landmarks:
        #     index_tip = landmarks[8]

        #     cv2.circle(
        #         frame,
        #         (index_tip["x"], index_tip["y"]),
        #         10,
        #         (255, 0, 255),
        #         cv2.FILLED,
        #     )

        #     print(
        #         "Index Tip:",
        #         index_tip["x"],
        #         index_tip["y"]
        #     )

        elif len(hands) == 2:

            hand1 = hands[0]
            hand2 = hands[1]

            index1 = hand1[8]
            index2 = hand2[8]

            x1 = min(index1["x"], index2["x"])
            x2 = max(index1["x"], index2["x"])

            y1 = min(index1["y"], index2["y"])

            frame_width = x2 - x1

            if frame_width < 250:
                status = "Move hands apart"
                status_color = (0, 165, 255)

            else:
                frame_height = 300
                y2 = y1 + frame_height

                h, w, _ = frame.shape

                x1 = max(0, x1)
                y1 = max(0, y1)

                x2 = min(w, x2)
                y2 = min(h, y2)

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    "CAPTURE AREA",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                status = "FRAME DETECTED"
                status_color = (0, 255, 0)
                thumb1 = hand1[4]
                index1 = hand1[8]

                thumb2 = hand2[4]
                index2 = hand2[8]

                pinch1 = tracker.calculate_distance(
                    thumb1,
                    index1
                )

                pinch2 = tracker.calculate_distance(
                    thumb2,
                    index2
                )

                pinch_threshold = 30
                is_pinching = (
                    pinch1 < pinch_threshold
                    or
                    pinch2 < pinch_threshold
                )

                current_capture_time = time.time()
                if (
                    is_pinching
                    and
                    current_capture_time - last_capture_time > capture_cooldown
                ):
                    captured_image = frame[y1:y2, x1:x2].copy()
                    cv2.imwrite(
                        "screenshots/captured_image.jpg",
                        captured_image
                    )

                    generator = PuzzleGenerator(grid_size=3)
                    tiles = generator.generate_tiles()
                    shuffled_tiles = generator.shuffle_tiles(tiles)

                    cap.release()
                    cv2.destroyAllWindows()

                    game = PuzzleGame(
                        shuffled_tiles,
                        grid_size=3
                    )

                    game.run()
                    break

                    flash_frame = frame.copy()
                    flash_frame[:] = (255, 255, 255)

                    cv2.imshow(
                        "Frame & Solve",
                        flash_frame
                    )

                    cv2.waitKey(120)

                    last_capture_time = current_capture_time

                    status = "PHOTO CAPTURED!"
                    status_color = (255, 255, 0)
                

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
        draw_status(frame, status, status_color)
        cv2.imshow("Frame & Solve", frame)

        key = cv2.waitKey(1)

        if key & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()