import numpy as np
from .mvnet import MoveNet

class Converter:

    def __init__(self):

        self.class_output = -1
        self.momentum = MoveNet.MOMENTUM.value
        self.threshold = MoveNet.CONFIDENCE_THRESHOLD.value
        self.previous = np.zeros(MoveNet.INPUT_SIZE.value)
        self.mvmt = np.zeros(MoveNet.INPUT_SIZE.value)

    def convert(self, keypoints):

        return keypoints

def get_converter(task: str):
    return Converter()