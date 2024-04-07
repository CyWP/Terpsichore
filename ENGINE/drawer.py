from .timer import Timer, Actions
from .mvnet import MoveNet
from appstate import AppState
import cv2
import numpy as np
import time
#import copy

class VoidDrawer:
    """
    A drawer class that performs no drawing.
    """

    def __init__(self, cap: cv2.VideoCapture):
        """
        Initializes the VoidDrawer.

        Args:
            cap (cv2.VideoCapture): VideoCapture object for capturing frames.
        """
        self.use_webcam = AppState.get_attr('webcam_active')
        self.delay = AppState.get_attr('delay')
        self.cap = cap
        self.win_name = MoveNet.WINDOW_NAME.value
        self.font = MoveNet.FONT.value
        self.font_color = MoveNet.FONT_COLOR.value
        self.font_scale = MoveNet.FONT_SCALE.value
        self.font_loc = MoveNet.FONT_LOCATION.value

    def output(self, frame, keypoints):
        """
        Placeholder method for outputting frame with keypoints.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.

        Returns:
            The output frame.
        """
        return frame

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
        
        while not Timer.is_done(timer_index):
            ret, frame = self.cap.read()  # Read a new frame
            if ret:
                if self.use_webcam:
                    ret, frame = self.cap.read()
                remaining_time = max(0, self.delay - time.time() + timer_start)
                text = f'{remaining_time:.2f}s'  # Format remaining time
                cv2.putText(frame, text, self.font_loc, self.font, self.font_scale, self.font_color, 2, cv2.LINE_4)
                cv2.imshow(self.win_name, frame)
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break  # Break the loop if 'q' is pressed
            else:
                break  # Break the loop if there's an issue reading frames

class FrameDrawer(VoidDrawer):
    """
    Drawer class for drawing frames.
    """

    def draw(self, frame, keypoints):
        """
        Draws keypoints on the frame.

        Args:
            frame: The input frame.
            keypoints: Detected keypoints.
        """
        cv2.imshow(self.win_name, self.output(frame, keypoints))

class KPDrawer(FrameDrawer):
    """
    Drawer class for drawing keypoints on frames.
    """
    def __init__(self, cap:cv2.VideoCapture):
        super().__init__(cap)
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
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))       
        for kp in shaped:
            ky, kx, kp_conf = kp
            cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1)

        for edge, color in self.edges.items():
            p1, p2, col = edge
            y1, x1, _ = shaped[p1]
            y2, x2, _ = shaped[p2]
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), col, 2)
        return frame

def get_drawer(cap: cv2.VideoCapture):
    """
    Factory function to get the appropriate drawer based on the application state.

    Args:
        cap (cv2.VideoCapture): VideoCapture object for capturing frames.

    Returns:
        Drawer: An instance of the appropriate drawer.
    """
    print(AppState.get_attr('show'))
    if not AppState.get_attr('show'):
        return VoidDrawer(cap)
    if AppState.get_attr('show_pose'):
        return KPDrawer(cap)
    else:
        return FrameDrawer(cap)