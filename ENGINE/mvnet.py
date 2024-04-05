import tensorflow as tf
import numpy as np
import cv2
import time
from dispatcher import Dispatcher, CSVWriter, OSCClient
from ..appstate import AppState
from math import dist
from .timer import Timer

class Engine():

    _edges = {
        (0, 1, (0, 255, 0)): 'm',
        (0, 2, (0, 0, 255)): 'c',
        (1, 3, (0, 0, 255)): 'm',
        (2, 4, (0, 0, 255)): 'c',
        (0, 5, (0, 0, 255)): 'm',
        (0, 6, (0, 0, 255)): 'c',
        (5, 7, (0, 255, 0)): 'm', #left bicep
        (7, 9,(0, 125, 0)): 'm', #left forearm
        (6, 8, (255, 0, 0)): 'c', #right biecep
        (8, 10, (125, 0, 0)): 'c', #right forearm
        (5, 6, (255, 255, 255)): 'y', #collarbone
        (5, 11, (0, 0, 255)): 'm',
        (6, 12, (0, 0, 255)): 'c',
        (11, 12, (255, 255, 255)): 'y', #hips
        (11, 13, (0, 255, 255)): 'm', #left thigh
        (13, 15,(0, 125, 125)): 'm', #left tibia
        (12, 14, (255, 0, 255)): 'c', #right thigh
        (14, 16, (125, 0, 125)): 'c' #right tibia
        }
    
    _keypoints = {
        'nose': 0,
        'left_eye': 1,
        'right_eye': 2,
        'left_ear': 3,
        'right_ear': 4,
        'left_shoulder': 5,
        'right_shoulder': 6,
        'left_elbow': 7,
        'right_elbow': 8,
        'left_wrist': 9,
        'right_wrist': 10,
        'left_hip': 11,
        'right_hip': 12,
        'left_knee': 13,
        'right_knee': 14,
        'left_ankle': 15,
        'right_ankle': 16}

    
    _momentum = 0.2 
    
    _confidence = 0.2 #confidence threshold for value to be deemed valid
    
    _frames = 0 #keeps track of frames

    _tf_model_path = "" #implement later

    @classmethod
    def launch(_cls, task:str):
    #Load Model
        interpreter = tf.lite.Interpreter(model_path=_cls._tf_model_path)
        interpreter.allocate_tensors()

        #init necessary variables
        dispatcher = select_dispatcher(task)
        use_webcam = AppState.get_attr('use_webcam')
        show = AppState.get_attr('show')
        delay = AppState.get_attr('delay')

        #Set Input device
        if use_webcam:
            try:
                cap = cv2.VideoCapture(AppState.get_attr('webcam_index'))
            except:
                cap = cv2.VideoCapture(0) #Switch to default webcam if specified index not working
        else:
            cap = cv2.VideoCapture(AppState.get_attr('video_path'))

        countdown(delay=delay,
                  video_capture=cap,
                  use_webcam=use_webcam) #Delays start of video input

        while cap.isOpened():

            ret, frame = cap.read()
            if frame is None:
                break
            # Reshape image
            img = frame.copy()
            img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192,192)
            input_image = tf.cast(img, dtype=tf.float32)
            # Setup input and output 
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            # Make predictions 
            interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
            interpreter.invoke()
            keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
            #Send to wekinator
            pose = format_tensor(keypoints_with_scores)
            direction = pose_to_vector(keypoints_with_scores)
            #blendclient.send_message("/vector", extract_direction(out))
            blendclient.send_message("/vec", direction)
            wekclient.send_message("/wek/inputs", pose)
            frames += 1
            # Rendering 
            if show:
                draw_connections(frame, keypoints_with_scores, EDGES, CONFIDENCE)
                draw_keypoints(frame, keypoints_with_scores, CONFIDENCE)
                cv2.imshow('Press q to quit', frame)
            #Press q to exit
            if cv2.waitKey(10) & 0xFF==ord('q') or (webcam and time.time()-start>=duration):
                break
        endclient.send_message("/end", 1)           
        cap.release()
        cv2.destroyAllWindows()

    def draw_keypoints(frame, keypoints, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y,x,1]))       
        for kp in shaped:
            ky, kx, kp_conf = kp
            if kp_conf > confidence_threshold:
                cv2.circle(frame, (int(kx), int(ky)), 4, (0,255,0), -1) 

    def draw_connections(frame, keypoints, edges, confidence_threshold):
        y, x, c = frame.shape
        shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))
        
        for edge, color in edges.items():
            p1, p2, col= edge
            y1, x1, c1 = shaped[p1]
            y2, x2, c2 = shaped[p2]
            
            if (c1 > confidence_threshold) & (c2 > confidence_threshold):      
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), col, 2)


def select_dispatcher(task:str, props:dict):
    
    if task=='move':
        return OSCClient(props['osc_port'])
    if task=='record':
        return CSVWriter() #TODO: create csv path generator
#Just returns a flat array of 34 floats
def format_tensor(keypoints):
    return np.asarray(np.delete(keypoints[0], np.s_[::3], None), dtype=float)

#Pathetic way to extract an estimation of the direction of the fastest moving extremity, estimates 3d location from 2d data
def pose_to_vector(keypoints):
    index = (frames+1) % BUF_SIZE
    length = len(extremities)
    speeds = np.ndarray(shape=(length,))
    zero = [0, 0, 0]
    kp = keypoints[0][0]
    position = np.zeros(kp.shape, dtype=np.float32)
    #Set new values for each category
    for i in range(length):
        #get 3d vector of every extremity, implies interpolating y val
        position = [kp[extremities[i]][0], 0., kp[extremities[i]][1]]
        coreheight = 1.25*dist([kp[core[i]][0], kp[core[i]][1]],[kp[core[(i+2)%length]][0], kp[core[(i+2)%length]][1]])
        position[1] = coreheight*(1-(dist([kp[core[i]][0], kp[core[i]][1]], [kp[joints[i]][0], kp[joints[i]][1]])+dist([kp[joints[i]][0], kp[joints[i]][1]], [kp[extremities[i]][0], kp[extremities[i]][1]]))/coreheight)
        #Reverses y direction if facing backwards
        if kp[leftshoulder][0]>kp[rightshoulder][0]:
            position[1] *= -1
        #Adds delta value in buffer and saves position for next frame.
        delta_buffer[i][index] = position-prev_pos[i]
        prev_pos[i] = position
        #Register averaged speed
        speeds[i] = 0.1*dist(zero, delta_buffer[i][(index-3)%BUF_SIZE])+0.2*dist(zero, delta_buffer[i][(index-2)%BUF_SIZE])+0.3*dist(zero, delta_buffer[i][(index-1)%BUF_SIZE])+0.4*dist(zero, delta_buffer[i][(index)%BUF_SIZE])
    #find largest index
    maxsp = speeds[i]
    maxi = 0
    for i in range (len(speeds)):
        if speeds[i]>maxsp:
            maxsp = speeds[i]
            maxi = i
    #Set/reset counters, return 3d vector value
    global active
    global same_count
    global diff_count
    if maxi == active:
        same_count += 1
        if same_count == DIFF_RESET:
            diff_count = 0
    else:
        diff_count += 1
        same_count = 0
        if diff_count == DIFF_MAX:
            diff_count = 0
            active = maxi
    print(delta_buffer[active][index])
    return np.asarray(delta_buffer[active][index], dtype=float)


def display_text(frame, remaining_time):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0, 0, 255)
    prompt = f"{remaining_time:.2f}s"
    cv2.putText(frame, prompt, (50, 50), font, 1, color, 2, cv2.LINE_4)
    return frame

def countdown(delay: int, video_capture: cv2.VideoCapture, use_webcam:bool):

    ti = Timer.add_timer(delay)
    ret, frame = video_capture.read()
    
    while not Timer.is_done(ti, pop=True):
        if use_webcam: #We do not want the delay timer to be running the video
            ret, frame = video_capture.read()
        remaining_time = max(0, delay - time.time() + Timer.starts[0])
        frame = display_text(frame, remaining_time)
        cv2.imshow('Press q to quit', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return
        
