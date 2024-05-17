import tensorflow as tf
import numpy as np
import cv2
from .dispatcher import get_dispatcher
from .drawer import get_drawer
from .converter import get_converter
from appstate import AppState
from .timer import Timer, Actions
from .mvnet import MoveNet
import threading
from terpsexception import TerpsException
import queue
import time
class Engine:
    """
    Class for running the engine that processes video input using MoveNet and performs actions based on detected movements and poses.
    """
    @classmethod
    async def launch(cls, task:str, after=lambda: None):
        """
        Launches the engine for processing video input.

        Args:
            task (str): The task type (e.g., "record" or "perform").
            after (function): Optional function to call after the engine completes execution.
        """
        err_queue = queue.Queue()

        def target_function(t, q):
            try:
                cls.launch_mvnet(t, q)
            except Exception as e:
                q.put(e)

        thread = threading.Thread(target=target_function, args=(task, err_queue))
        AppState.start_engine()
        thread.start()
        thread.join()
        after()

        while not err_queue.empty():
            error = err_queue.get()
            raise TerpsException(error)

    @classmethod
    def launch_mvnet(cls, task:str, err_queue:queue.Queue):
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
                interval = 0.0
                try:
                    cap = cv2.VideoCapture(AppState.get_attr('webcam_index'))
                except:
                    try:
                        cap = cv2.VideoCapture(0)  # Switch to default webcam if specified index not working
                    except Exception as e:
                        raise e
            else:
                cap = cv2.VideoCapture(AppState.get_attr('video_path'))
                fps = cap.get(cv2.CAP_PROP_FPS)
                interval = 1.0/fps if fps>0 else 0.0
                
            
            #init first frame, used to get certain variables
            ret, frame = cap.read()

            # Initialize necessary variables
            show = AppState.get_attr('show')
            duration = AppState.get_attr('duration')
            exit_key = MoveNet.EXIT_KEY.value
            win_name = MoveNet.WINDOW_NAME.value
            scr_x = MoveNet.SCREEN_X.value
            scr_y = MoveNet.SCREEN_Y.value
            custom_size = AppState.get_attr('custom_size')
            if custom_size:
                win_x = int(scr_x*AppState.get_attr('x_size')/100)
                win_y = int(scr_y*AppState.get_attr('y_size')/100)
            else:
                win_x = frame.shape[1]
                win_y = frame.shape[0]
            size = (win_x, win_y)
            x_loc = int(AppState.get_attr('x_loc') / 100 * (scr_x - win_x))
            y_loc = int(AppState.get_attr('y_loc') / 100 * (scr_y - win_y))

            # Initialize action classes
            dispatcher = get_dispatcher(task)
            drawer = get_drawer(cap, size)
            converter = get_converter(task)

            # Initialize window
            if show:
                cv2.imshow(win_name, frame)
                cv2.moveWindow(win_name, x_loc, y_loc)

            #initialize count down phase
            drawer.countdown()

            # Add timer
            main_timer = Timer.add_timer(duration=duration, action=Actions.POP)

            dispatcher.start()
            frame_time = 0

            #lots of things to check  for
            while cap.isOpened() and not AppState.engine_aborted() and ret and not(cv2.waitKey(10) & 0xFF == ord(exit_key)) and not(use_webcam and Timer.is_done(main_timer)):

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
                try:
                    mvmt, pose, gesture_class, extr = converter.convert(keypoints_with_scores)
                except Exception as e:
                    raise e
                
                # Render detected poses on the frame
                drawer.draw(frame, pose)
                
                # Dispatch movements, poses, and gestures
                dispatcher.dispatch(mvmt.ravel(), pose.ravel(), gesture_class, extr.ravel())
                
                #Pace video
                time.sleep(max(0, interval-time.time()+frame_time-0.01))

                #get new frame
                ret, frame = cap.read()
                frame_time = time.time()
                
            #final action for dispatcher
            dispatcher.close(err=False)

        except Exception as e:
            try: 
                #put in try block in case error occured before dispatcher was instantiated
                dispatcher.close(err=True)
            except:
                pass
            raise e
        
        finally:
            # Clean up and release resources, even if error occured. Order of these two matters.
            try:
                cap.release()
                cv2.destroyAllWindows()
            except Exception as e:
                raise e