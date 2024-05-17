from appstate import AppState
from os import path, listdir
import numpy as np
from .mvnet import MoveNet
import tensorflow as tf
import time
from keras.utils import to_categorical
from .classifier import get_classifier
import traceback
import threading
from sklearn.model_selection import train_test_split

class Trainer:

    @classmethod
    async def train(cls):
        threading.Thread(target=cls.train_model).start()

    @classmethod
    def train_model(cls):
            
        try:

            AppState.start_train()

            weights_path = AppState.get_model_checkpoint()
            test_split=AppState.get_attr('test_split')/100
            
            X, y, label_map = cls.preprocess()

            model = get_classifier()
            
            model.train(X, y)

            model.save(filepath=weights_path)

            AppState.update_model(label_map)

            time.sleep(1)#to let time for frame to get all logs

            AppState.end_train()
        
        except (Exception) as e:
            AppState.train_log(e)
            time.sleep(1)#to let time for frame to get all logs
            AppState.end_train()

    @classmethod
    def preprocess(cls):
        
        AppState.train_log('Initiated data preprocessing')
        #simply an array of gesture names, with the index being its corresponding label value(int, not one-hot encoded)
        gesture_names = []
        label_map = {}
        
        temporal_size = MoveNet.TEMPORAL_AXIS_SIZE.value

        X = []
        y = []

        for name, dirpath in AppState.get_gesture_paths():

            AppState.train_log(f'Preprocessing: {name}')

            gesture_names.append(name)
            label = len(gesture_names)-1
            label_map[name] = label
            #We only want csv files
            files = [path.join(dirpath, file) for file in listdir(dirpath) if file.endswith('.csv')]
               
            for file in files:
                recs = np.genfromtxt(file, delimiter=',')
                #Create windows of appropriate size
                for i in range(max(0, recs.shape[0]-temporal_size)):
                    X.append(recs[i:i+temporal_size, :])
                    y.append(label)

        X = tf.convert_to_tensor(X)
        y = tf.convert_to_tensor(y)

        AppState.train_log('Preprocessing Complete')

        return X, y, label_map