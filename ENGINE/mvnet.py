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

        MODELPATH = path.abspath('DATA/mvnet.tflite')

        INPUT_SIZE = 34

        NUM_POINTS = 17

        MOMENTUM = 0.2

        CONFIDENCE_THRESHOLD = 0.07

        POSE_COLOR = (0, 255, 0)

        LINE_THICKNESS = 2

        FONT = cv2.FONT_HERSHEY_SIMPLEX

        FONT_COLOR = (255, 255, 0)

        FONT_SCALE = 3

        FONT_LOCATION = (50, 100)

        INFERENCE_X = 192

        INFERENCE_Y = 192

        EXIT_KEY = 'q'

        WINDOW_NAME = f'Terpsichore: press {EXIT_KEY} to Exit'

        TEMPORAL_AXIS_SIZE = 17

        SCREEN_X = get_monitors()[0].width

        SCREEN_Y = get_monitors()[0].height

        '''def draw_keypoints(frame, keypoints, confidence_threshold):
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

    if delay <= 0:
        return
    
    ti = Timer.add_timer(delay, action='pop')
    ret, frame = video_capture.read()
    
    while not Timer.is_done(ti, pop=True):
        if use_webcam: #We do not want the delay timer to be running the video, just pause at the first frame
            ret, frame = video_capture.read()
        remaining_time = max(0, delay - time.time() + Timer.starts[0])
        frame = display_text(frame, remaining_time)
        cv2.imshow('Press q to quit', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            return'''
        
