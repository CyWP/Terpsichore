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

    @classmethod
    async def launch(_cls, task:str, after=lambda: None):

        #Load Model
        interpreter = tf.lite.Interpreter(model_path=MoveNet.MODELPATH.value)
        interpreter.allocate_tensors()

        use_webcam = AppState.get_attr('webcam_active')
        #Set Input device
        if use_webcam:
            try:
                cap = cv2.VideoCapture(AppState.get_attr('webcam_index'))
            except:
                cap = cv2.VideoCapture(0) #Switch to default webcam if specified index not working
        else:
            cap = cv2.VideoCapture(AppState.get_attr('video_path'))

        ret, frame = cap.read()

        #init necessary variables
        show = AppState.get_attr('show')
        duration = AppState.get_attr('duration')
        win_name = MoveNet.WINDOW_NAME.value
        win_x = frame.shape[1]
        win_y = frame.shape[2]
        scr_x = MoveNet.SCREEN_X.value
        scr_y = MoveNet.SCREEN_Y.value
        x_loc = int(AppState.get_attr('x_loc')/100*(scr_x-win_x))
        y_loc = int(AppState.get_attr('y_loc')/100*(scr_y-win_y))
        x_loc = 0
        y_loc=0
        print('hi')
        #init action classes
        dispatcher = get_dispatcher(task)
        drawer = get_drawer(cap)
        converter = get_converter(task)

        #Init window
        if show:
            cv2.imshow(win_name, frame)
            cv2.moveWindow(win_name, x_loc, y_loc)

        drawer.countdown()

        main_timer = Timer.add_timer(duration=duration, action=Actions.POP)

        while cap.isOpened():

            ret, frame = cap.read()
            if not ret:
                break
            # Reshape image
            img = frame.copy()
            img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), MoveNet.INFERENCE_X.value, MoveNet.INFERENCE_Y.value)
            input_image = tf.cast(img, dtype=tf.float32)

            # Setup input and output 
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # Make predictions 
            interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
            interpreter.invoke()
            keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])

            #Properly format output
            data = converter.convert(keypoints_with_scores)

            #Send output
            dispatcher.dispatch(data)

            # Rendering 
            drawer.draw(frame, keypoints_with_scores)
            
            #Press q to exit
            if cv2.waitKey(10) & 0xFF==ord('q') or (use_webcam and Timer.is_done(main_timer)):
                break

        dispatcher.close()         
        cap.release()
        cv2.destroyAllWindows()
        after()