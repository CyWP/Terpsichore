from .timer import Timer, Actions
from .mvnet import MoveNet
from appstate import AppState
import cv2
import numpy as np
import time
import copy


class VoidDrawer:
    """
    A drawer class that performs no drawing.
    """

    def __init__(self, cap: cv2.VideoCapture, size: tuple):
        """
        Initializes the VoidDrawer.

        Args:
            cap (cv2.VideoCapture): VideoCapture object for capturing frames.
        """
        self.use_webcam = AppState.get_attr("webcam_active")
        self.delay = AppState.get_attr("delay")
        self.cap = cap
        self.size = size
        self.win_name = MoveNet.WINDOW_NAME.value
        self.pose_color = MoveNet.POSE_COLOR.value
        self.line_thick = MoveNet.LINE_THICKNESS.value
        self.font = MoveNet.FONT.value
        self.font_color = MoveNet.FONT_COLOR.value
        self.font_scale = MoveNet.FONT_SCALE.value
        self.font_loc = MoveNet.FONT_LOCATION.value

    def output(self, frame, pose):
        """
        Placeholder method for outputting frame with keypoints.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.

        Returns:
            The output frame.
        """
        return cv2.resize(frame, self.size)

    def draw(self, frame, keypoints):
        """
        Placeholder method for drawing keypoints on frame.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.
        """
        pass

    def countdown(self):
        """
        Displays countdown on the frame.

        Args:
            frame: The frame to display countdown on.
        """
        if self.delay <= 0:
            return

        timer_start = time.time()  # Record the start time of the countdown
        timer_index = Timer.add_timer(duration=self.delay, action=Actions.POP)
        ret, frame = self.cap.read()  # Read a new frame
        baseframe = cv2.resize(copy.deepcopy(frame), self.size)

        while not Timer.is_done(timer_index):
            if ret:
                if self.use_webcam:
                    ret, frame = self.cap.read()
                    frame = cv2.resize(frame, self.size)
                else:
                    # We want to keep displaying the same first frame if the input is video
                    frame = copy.deepcopy(baseframe)
                remaining_time = max(0, self.delay - time.time() + timer_start)
                text = f"{remaining_time:.2f}s"  # Format remaining time
                cv2.putText(
                    frame,
                    text,
                    self.font_loc,
                    self.font,
                    self.font_scale,
                    self.font_color,
                    self.line_thick,
                    cv2.LINE_4,
                )
                cv2.imshow(self.win_name, frame)
                if cv2.waitKey(10) & 0xFF == ord("q"):
                    break  # Break the loop if 'q' is pressed
            else:
                break  # Break the loop if there's an issue reading frames


class FrameDrawer(VoidDrawer):
    """
    Drawer class for drawing frames.
    """

    def draw(self, frame, points):
        """
        Draws keypoints on the frame.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.
        """
        cv2.imshow(self.win_name, self.output(cv2.resize(frame, self.size), points))


class KPDrawer(FrameDrawer):
    """
    Drawer class for drawing keypoints on frames.
    """

    def __init__(self, cap: cv2.VideoCapture, size: tuple):
        super().__init__(cap, size)
        self.edges = MoveNet.EDGES.value

    def output(self, frame, keypoints):
        """
        Outputs frame with keypoints drawn.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.

        Returns:
            The output frame.
        """
        frame = super().output(frame, keypoints)

        shaped = np.multiply(keypoints, np.array(self.size)).astype(int)

        for edge in self.edges:
            p1, p2 = edge
            y1, x1 = shaped[p1]
            y2, x2 = shaped[p2]
            cv2.line(frame, (x1, y1), (x2, y2), self.pose_color, self.line_thick)
        return frame


def get_drawer(cap: cv2.VideoCapture, size: tuple):
    """
    Factory function to get the appropriate drawer based on the application state.

    Args:
        cap (cv2.VideoCapture): VideoCapture object for capturing frames.

    Returns:
        Drawer: An instance of the appropriate drawer.
    """

    if not AppState.get_attr("show"):
        return VoidDrawer(cap, size)
    if AppState.get_attr("show_pose"):
        return KPDrawer(cap, size)
    else:
        return FrameDrawer(cap, size)
