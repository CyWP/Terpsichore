import tensorflow as tf
import numpy as np
import cv2
from .dispatcher import get_dispatcher
from .drawer import get_drawer
from .converter import get_converter
from appstate import AppState
from .timer import Timer, Actions
from .mvnet import MoveNet
import asyncio

class Engine:
    """
    Class for running the engine that processes video input using MoveNet and performs actions based on detected movements and poses.
    """

    @classmethod
    async def launch(_cls, task:str, after=lambda: None):
        """
        Launches the engine for processing video input.

        Args:
            task (str): The task type (e.g., "record" or "perform").
            after (function): Optional function to call after the engine completes execution.
        """

        try:
            # Load MoveNet model
            interpreter = tf.lite.Interpreter(model_path=MoveNet.MODELPATH.value)
            interpreter.allocate_tensors()

            # Determine input device (webcam or video file)
            use_webcam = AppState.get_attr('webcam_active')
            if use_webcam:
                try:
                    cap = cv2.VideoCapture(AppState.get_attr('webcam_index'))
                except:
                    cap = cv2.VideoCapture(0)  # Switch to default webcam if specified index not working
            else:
                cap = cv2.VideoCapture(AppState.get_attr('video_path'))
            
            #init first frame, used to get certain variables
            ret, frame = cap.read()

            # Initialize necessary variables
            show = AppState.get_attr('show')
            duration = AppState.get_attr('duration')
            exit_key = MoveNet.EXIT_KEY.value
            win_name = MoveNet.WINDOW_NAME.value
            win_x = frame.shape[1]
            win_y = frame.shape[2]
            scr_x = MoveNet.SCREEN_X.value
            scr_y = MoveNet.SCREEN_Y.value
            x_loc = int(AppState.get_attr('x_loc') / 100 * (scr_x - win_x))
            y_loc = int(AppState.get_attr('y_loc') / 100 * (scr_y - win_y))
            x_loc = 0
            y_loc = 0

            # Initialize action classes
            dispatcher = get_dispatcher(task)
            drawer = get_drawer(cap)
            converter = get_converter(task)

            # Initialize window
            if show:
                cv2.imshow(win_name, frame)
                cv2.moveWindow(win_name, x_loc, y_loc)

            #initialize count down phase
            drawer.countdown()

            print(frame)

            # Add timer
            main_timer = Timer.add_timer(duration=duration, action=Actions.POP)

            #lots of things to check  for
            while cap.isOpened() and ret and not(cv2.waitKey(10) & 0xFF == ord(exit_key)) and not(use_webcam and Timer.is_done(main_timer)):

                # Reshape image and preprocess
                img = frame.copy()
                img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), MoveNet.INFERENCE_X.value, MoveNet.INFERENCE_Y.value)
                input_image = tf.cast(img, dtype=tf.float32)
                
                # Setup input and output details for the interpreter
                input_details = interpreter.get_input_details()
                output_details = interpreter.get_output_details()
                
                # Make predictions using MoveNet model
                interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
                interpreter.invoke()
                keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
                
                # Convert keypoints to movements, poses, and gestures
                mvmt, pose, gesture_class = converter.convert(keypoints_with_scores)
                
                # Render detected poses on the frame
                drawer.draw(frame, pose)
                
                # Dispatch movements, poses, and gestures
                dispatcher.dispatch(mvmt.ravel(), pose.ravel(), gesture_class)
                
                #get new frame
                ret, frame = cap.read()
                
            #final action for dispatcher
            dispatcher.close(err=False)

        except Exception as e:

            print("An error occurred:", e)

            try: 
                #put in try block in case error occured before dispatcher was instantiated
                dispatcher.close(err=True)
            except:
                pass
        finally:
            # Clean up and release resources, even if error occured. Order of these two matters.
            try:
                cap.release()
                cv2.destroyAllWindows()
            except:
                pass
            #this should always be able to run, app is cooked if it can't
            after()