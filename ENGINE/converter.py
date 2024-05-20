import numpy as np
from numpy.linalg import norm
from .mvnet import MoveNet
import tensorflow as tf
from .tasks import Tasks
from appstate import AppState
import traceback
from terpsexception import TerpsException
from appstate import AppState


class Converter:
    """
    Base class for converting keypoints with scores to movement, pose, and class output.
    """

    def __init__(self):
        """
        Initializes Converter object with default values.
        """
        self.class_output = tf.convert_to_tensor(-1 * np.ones((1,)))
        self.momentum = AppState.get_attr("momentum")
        self.threshold = AppState.get_attr("conf_threshold")
        self.pose = np.zeros((MoveNet.NUM_POINTS.value, 2))
        self.mvmt = np.zeros((MoveNet.NUM_POINTS.value, 2))
        self.ext_mvmt = np.zeros((4, 3))

    def convert(self, keypoints_with_scores):
        """
        Converts keypoints with scores to movement, pose, and class output.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.

        Returns:
            tuple: Tuple containing movement, pose, and class output.
        """
        self.compute_output(keypoints_with_scores)
        return self.mvmt, self.pose, self.class_output.numpy(), self.ext_mvmt

    def compute_output(self, keypoints_with_scores):
        """
        Computes movement, pose, and class output.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.
        """
        keypoints_with_scores = np.reshape(
            keypoints_with_scores, keypoints_with_scores.shape[-2:]
        )
        keypoints = keypoints_with_scores[:, :-1]
        threshold_mask = (keypoints_with_scores[:, -1] > self.threshold)[:, np.newaxis]
        self.mvmt = (
            self.momentum * self.mvmt
            + (1 - self.momentum) * (keypoints - self.pose) * threshold_mask
            + self.mvmt * ~threshold_mask
        )
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
        try:
            self.classifier = tf.keras.models.load_model(
                AppState.get_model_checkpoint()
            )
        except Exception as e:
            traceback.print_exc()
            raise TerpsException(f"Error: no model has been trained.")

        self.class_input = np.zeros(self.classifier.input_shape[1:])

        self.class_output = np.zeros(self.classifier.output_shape[-1])
        kpi = MoveNet.KEYPOINTS.value
        self.ext_indices = [
            kpi["right_wrist"],
            kpi["left_wrist"],
            kpi["right_ankle"],
            kpi["left_ankle"],
        ]
        self.joint_indices = [
            kpi["right_elbow"],
            kpi["left_elbow"],
            kpi["right_knee"],
            kpi["left_knee"],
        ]
        self.hinge_indices = [
            kpi["right_shoulder"],
            kpi["left_shoulder"],
            kpi["right_hip"],
            kpi["left_hip"],
        ]
        self.bust_indices = [kpi["right_shoulder"], kpi["right_hip"]]
        self.ext = np.zeros((4, 3))
        self.ext_mvmt = np.zeros((4, 3))

    def compute_output(self, keypoints_with_scores):
        """
        Computes movement, pose, and class output including classification.

        Args:
            keypoints_with_scores (ndarray): Keypoints with scores.
        """
        super().compute_output(keypoints_with_scores)

        self.class_input = np.concatenate(
            [self.class_input, self.mvmt.ravel()[np.newaxis, :]]
        )[1:, :]

        self.class_output = self.classifier.call(
            tf.convert_to_tensor(self.class_input[None, ...])
        )

        self.compute_extremities()

    def compute_extremities(self):
        """
        Estimates 3d direction vector of extremities (wrists and ankles)
        """

        hinges = self.pose[self.hinge_indices, :]
        joints = self.pose[self.joint_indices, :]
        exts = self.pose[self.ext_indices, :]

        refs = norm(hinges - joints, axis=-1) + norm(joints - exts, axis=-1)
        bustlengths = norm(np.diff(self.pose[self.bust_indices, :])) * np.ones(
            shape=(refs.shape)
        )
        refs = np.mean(
            np.max(np.moveaxis(np.stack((refs, bustlengths), axis=-1), -1, 0), axis=0)
        ) * np.ones((4,))

        l1 = norm(
            np.stack([norm(hinges - joints, axis=-1), refs / 2], axis=-1), axis=-1
        )

        l2 = norm(np.stack([norm(joints - exts, axis=-1), refs / 2], axis=-1), axis=-1)

        l2_dir = (-1.0, 1.0)[
            norm(hinges - joints) > 1.1 * norm(joints - exts)
        ] * np.array([-1.0, -1.0, 1.0, 1.0])
        pose_dir = (-1.0, 1.0)[hinges[1, 0] < hinges[0, 0]]

        poses = np.hstack((exts, (pose_dir * (l1 + l2_dir * l2))[:, np.newaxis]))
        self.ext_mvmt = poses - self.ext
        self.ext = poses


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
