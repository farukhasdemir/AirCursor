from __future__ import annotations

import argparse
import math
import time
from dataclasses import dataclass

import cv2
import mediapipe as mp
import pyautogui


PINCH_THRESHOLD = 0.045
CLICK_COOLDOWN_SECONDS = 0.35


@dataclass
class GestureState:
    last_left_click: float = 0.0
    last_right_click: float = 0.0
    dragging: bool = False
    smooth_x: float | None = None
    smooth_y: float | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Control the mouse with hand gestures through your webcam."
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index, usually 0.")
    parser.add_argument(
        "--smoothing",
        type=float,
        default=0.28,
        help="Pointer smoothing from 0.05 to 1.0. Higher is faster.",
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=0.12,
        help="Ignored camera edge margin. Helps reach screen edges comfortably.",
    )
    parser.add_argument(
        "--mirror",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Mirror the camera view.",
    )
    return parser.parse_args()


def distance(a, b) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def map_to_screen(value: float, size: int, margin: float) -> int:
    normalized = (value - margin) / (1.0 - (2.0 * margin))
    normalized = min(1.0, max(0.0, normalized))
    return int(normalized * size)


def smooth(current: float, target: float, amount: float) -> float:
    return current + ((target - current) * amount)


def put_help(frame, status: str) -> None:
    lines = [
        "Index finger: move",
        "Thumb + index: left click",
        "Thumb + middle: right click",
        "Thumb + ring: drag",
        "Q: quit",
    ]
    y = 28
    for line in lines:
        cv2.putText(
            frame,
            line,
            (12, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.62,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )
        y += 28

    cv2.putText(
        frame,
        status,
        (12, frame.shape[0] - 18),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (80, 255, 120),
        2,
        cv2.LINE_AA,
    )


def main() -> int:
    args = parse_args()
    pyautogui.FAILSAFE = True
    screen_w, screen_h = pyautogui.size()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Camera could not be opened. Try another camera index with --camera 1.")
        return 1

    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    state = GestureState()

    with mp_hands.Hands(
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.72,
        min_tracking_confidence=0.72,
    ) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Camera frame could not be read.")
                return 1

            if args.mirror:
                frame = cv2.flip(frame, 1)

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            status = "No hand"

            if result.multi_hand_landmarks:
                landmarks = result.multi_hand_landmarks[0]
                lm = landmarks.landmark

                index_tip = lm[8]
                thumb_tip = lm[4]
                middle_tip = lm[12]
                ring_tip = lm[16]

                target_x = map_to_screen(index_tip.x, screen_w, args.margin)
                target_y = map_to_screen(index_tip.y, screen_h, args.margin)

                if state.smooth_x is None or state.smooth_y is None:
                    state.smooth_x = target_x
                    state.smooth_y = target_y
                else:
                    state.smooth_x = smooth(state.smooth_x, target_x, args.smoothing)
                    state.smooth_y = smooth(state.smooth_y, target_y, args.smoothing)

                pyautogui.moveTo(int(state.smooth_x), int(state.smooth_y), duration=0)

                now = time.monotonic()
                left_pinch = distance(thumb_tip, index_tip) < PINCH_THRESHOLD
                right_pinch = distance(thumb_tip, middle_tip) < PINCH_THRESHOLD
                drag_pinch = distance(thumb_tip, ring_tip) < PINCH_THRESHOLD

                if drag_pinch:
                    if not state.dragging:
                        pyautogui.mouseDown()
                        state.dragging = True
                    status = "Dragging"
                else:
                    if state.dragging:
                        pyautogui.mouseUp()
                        state.dragging = False
                    status = "Moving"

                if left_pinch and now - state.last_left_click > CLICK_COOLDOWN_SECONDS:
                    pyautogui.click(button="left")
                    state.last_left_click = now
                    status = "Left click"

                if right_pinch and now - state.last_right_click > CLICK_COOLDOWN_SECONDS:
                    pyautogui.click(button="right")
                    state.last_right_click = now
                    status = "Right click"

                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            put_help(frame, status)
            cv2.imshow("Hand Mouse Control", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    if state.dragging:
        pyautogui.mouseUp()
    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
