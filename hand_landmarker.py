import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import pygame

model_path = "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

HAND_EVENT = pygame.USEREVENT + 1


def get_index_landmark(result):
    if result.hand_landmarks:
        hand_landmarks_hands = result.hand_landmarks
        hand_landmarks_list = hand_landmarks_hands[0]
        return hand_landmarks_list[8]


def print_result(
    result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int
):
    if get_index_landmark(result):
        delta_x = get_index_landmark(result).x - 0.5
        delta_y = get_index_landmark(result).y - 0.5
        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                print("right")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "R"}))
            else:
                print("left")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "L"}))
        else:
            if delta_y > 0:
                print("down")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "D"}))
            else:
                print("up")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "U"}))


def run():
    options = vision.HandLandmarkerOptions(
        base_options=python.BaseOptions(model_asset_path=model_path),
        num_hands=1,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result,
    )
    with vision.HandLandmarker.create_from_options(options) as landmarker:
        vid = cv2.VideoCapture(0)

        while True:
            ret, frame = vid.read()
            frame = cv2.flip(frame, 1)

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            landmarker.detect_async(mp_image, int(vid.get(cv2.CAP_PROP_POS_MSEC)))

            height, width, _ = frame.shape
            cv2.line(frame, (0, 0), (width, height), (0, 255, 0), 1)
            cv2.line(frame, (0, height), (width, 0), (0, 255, 0), 1)
            frame = cv2.resize(frame, None, fx=0.8, fy=0.8)
            cv2.imshow("frame", frame)

            cv2.moveWindow("frame", 0, 0)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        vid.release()
        cv2.destroyAllWindows()
