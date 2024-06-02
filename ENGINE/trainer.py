from appstate import AppState
from os import path, listdir
import numpy as np
import tensorflow as tf
import time
from .classifier import get_classifier
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
            test_split = AppState.get_attr("test_split") / 100
            temporal_size = AppState.get_attr("temporal_size")

            X_trn, y_trn, X_val, y_val, label_map = cls.preprocess(test_split, temporal_size)

            model = get_classifier()

            model.train(X_trn, y_trn, X_val, y_val)

            if not AppState._abort_training:
                model.save(filepath=weights_path)

            AppState.update_model(label_map)

            #Reset values
            AppState.reset_training()

            time.sleep(1)  # to let time for frame to get all logs

            AppState.end_train()

        except Exception as e:
            AppState.train_log(e)
            time.sleep(1)  # to let time for frame to get all logs
            AppState.end_train()

    @classmethod
    def preprocess(cls, test_split, temporal_size):

        AppState.train_log("Initiated data preprocessing")
        # simply an array of gesture names, with the index being its corresponding label value(int, not one-hot encoded)
        gesture_names = []
        label_map = {}

        X = []
        y = []

        for name, dirpath in AppState.get_gesture_paths():

            AppState.train_log(f"Preprocessing: {name}")

            gesture_names.append(name)
            label = len(gesture_names) - 1
            label_map[name] = label
            # We only want csv files
            files = [
                path.join(dirpath, file)
                for file in listdir(dirpath)
                if file.endswith(".csv")
            ]

            for file in files:
                recs = np.genfromtxt(file, delimiter=",")
                # Create windows of appropriate size
                for i in range(max(0, recs.shape[0] - temporal_size)):
                    X.append(recs[i : i + temporal_size, :])
                    y.append(label)

        X = np.expand_dims(np.array(X), -1)
        y = np.expand_dims(np.array(y), -1)

        if test_split > 0.0:
            AppState.train_log("Splitting datasets")
            X_trn, X_val, y_trn, y_val = train_test_split(X, y, test_size=test_split)
            print(X_trn.shape)
            AppState.train_log("Preprocessing Complete")
            return tf.convert_to_tensor(X_trn), tf.convert_to_tensor(y_trn), tf.convert_to_tensor(X_val), tf.convert_to_tensor(y_val), label_map
        else:
            AppState.train_log("Preprocessing Complete")
            return tf.convert_to_tensor(X), tf.convert_to_tensor(y), None, None, label_map
