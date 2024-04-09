import numpy as np
from .mvnet import MoveNet
import tensorflow as tf
from .classifier import get_classifier
from .tasks import Tasks
from appstate import AppState
class Converter:
    """
    Base class for converting keypoints with scores to movement, pose, and class output.
    """

    def __init__(self):
        """
        Initializes Converter object with default values.
        """
        self.class_output = np.zeros((1,))
        self.momentum = MoveNet.MOMENTUM.value
        self.threshold = MoveNet.CONFIDENCE_THRESHOLD.value
        self.pose = np.zeros((MoveNet.NUM_POINTS.value, 2))
        self.mvmt = np.zeros((MoveNet.NUM_POINTS.value, 2))

    def convert(self, keypoints_with_scores):
        """
        Converts keypoints with scores to movement, pose, and class output.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.

        Returns:
            tuple: Tuple containing movement, pose, and class output.
        """
        self.compute_output(keypoints_with_scores)
        return self.mvmt, self.pose, self.class_output
    
    def compute_output(self, keypoints_with_scores):
        """
        Computes movement, pose, and class output.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.
        """
        keypoints_with_scores = np.reshape(keypoints_with_scores, keypoints_with_scores.shape[-2:])
        keypoints = keypoints_with_scores[:, :-1]
        threshold_mask = (keypoints_with_scores[:, -1] > self.threshold)[:, np.newaxis]
        self.mvmt = self.momentum*self.mvmt +(1-self.momentum)*(keypoints - self.pose) * threshold_mask + self.mvmt * ~threshold_mask
        self.pose += self.mvmt

class ConverterClassifier(Converter):
    """
    Subclass of Converter that adds classification functionality.
    """

    def __init__(self):
        """
        Initializes ConverterClassifier object with default values.
        """
        super().__init__()
        self.class_output = np.zeros((AppState.get_num_classes(),))
        self.classifier = get_classifier()  # Assuming get_classifier() returns a classifier model
    
    def compute_output(self, keypoints_with_scores):
        """
        Computes movement, pose, and class output including classification.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.
        """
        super().compute_output(keypoints_with_scores)
        self.class_output = self.classifier.predict()

def get_converter(task: str):
    """
    Factory function to get a converter based on the specified task.

    Args:
        task (str): The task type.

    Returns:
        Converter: Converter object based on the task.
    """
    if task == Tasks.RECORD:
        return Converter()
    elif task == Tasks.PERFORM:
        return ConverterClassifier()