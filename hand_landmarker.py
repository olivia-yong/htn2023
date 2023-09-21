import mediapipe as mp
import cv2
import pygame

MODEL_PATH = "hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

HAND_EVENT = pygame.USEREVENT + 1


# Identify the tip of the index finger
def get_index_landmark(result):
    INDEX_LANDMARK = 8
    if result.hand_landmarks:
        hand_landmarks_hands = result.hand_landmarks
        hand_landmarks_list = hand_landmarks_hands[0]
        return hand_landmarks_list[INDEX_LANDMARK]


# Print the result of the hand gesture and trigger pygame event
def print_result(
    result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int
):
    if get_index_landmark(result):
        # calculate horizontal and vertical movement
        delta_x = get_index_landmark(result).x - 0.5
        delta_y = get_index_landmark(result).y - 0.5

        # horizontal movement greater than vertical movement
        if abs(delta_x) > abs(delta_y):
            if delta_x > 0:
                print("right")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "R"}))
            else:
                print("left")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "L"}))

        # vertical movement greater than horizontal movement
        else:
            if delta_y > 0:
                print("down")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "D"}))
            else:
                print("up")
                pygame.event.post(pygame.event.Event(HAND_EVENT, {"result": "U"}))


# Start the hand landmarker
def run():
    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=1,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result,
    )
    with HandLandmarker.create_from_options(options) as landmarker:
        vid = cv2.VideoCapture(0)

        while True:
            # read the video frame
            ret, frame = vid.read()

            # mirror
            frame = cv2.flip(frame, 1)

            # format frame to mp image and detect hand landmarks
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            landmarker.detect_async(mp_image, int(vid.get(cv2.CAP_PROP_POS_MSEC)))

            # draw green lines separating directions for live video view
            height, width, _ = frame.shape
            cv2.line(frame, (0, 0), (width, height), (0, 255, 0), 2)
            cv2.line(frame, (0, height), (width, 0), (0, 255, 0), 2)

            # resize the video view
            frame = cv2.resize(frame, None, fx=0.8, fy=0.8)

            # show the video
            cv2.imshow("frame", frame)

            # move the video view to the top left corner
            cv2.moveWindow("frame", 0, 0)

            # quite if q key pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        vid.release()
        cv2.destroyAllWindows()
