import cv2
from enum import Enum
from screeninfo import get_monitors
from os import path


class MoveNet(Enum):

    EDGES = (
        (0, 1),
        (0, 2),
        (1, 3),
        (2, 4),
        (0, 5),
        (0, 6),
        (5, 7),
        (7, 9),
        (6, 8),
        (8, 10),
        (5, 6),
        (5, 11),
        (6, 12),
        (11, 12),
        (11, 13),
        (13, 15),
        (12, 14),
        (14, 16),
    )

    KEYPOINTS = {
        "nose": 0,
        "left_eye": 1,
        "right_eye": 2,
        "left_ear": 3,
        "right_ear": 4,
        "left_shoulder": 5,
        "right_shoulder": 6,
        "left_elbow": 7,
        "right_elbow": 8,
        "left_wrist": 9,
        "right_wrist": 10,
        "left_hip": 11,
        "right_hip": 12,
        "left_knee": 13,
        "right_knee": 14,
        "left_ankle": 15,
        "right_ankle": 16,
    }

    MODELPATH = path.abspath("DATA/mvnet.tflite")

    INPUT_SIZE = 34

    NUM_POINTS = 17

    POSE_COLOR = (0, 255, 0)

    LINE_THICKNESS = 2

    FONT = cv2.FONT_HERSHEY_SIMPLEX

    FONT_COLOR = (255, 255, 0)

    FONT_SCALE = 3

    FONT_LOCATION = (50, 100)

    INFERENCE_X = 192

    INFERENCE_Y = 192

    EXIT_KEY = "q"

    WINDOW_NAME = f"Terpsichore: press {EXIT_KEY} to Exit"

    TEMPORAL_AXIS_SIZE = 17

    SCREEN_X = get_monitors()[0].width

    SCREEN_Y = get_monitors()[0].height
