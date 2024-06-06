from appstate import AppState
from ENGINE.mvnet import MoveNet
from os import path, listdir
import numpy as np
import tensorflow as tf
import time
from .classifier import get_classifier
import threading
from sklearn.model_selection import train_test_split
import copy

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

            if not AppState._cancel_training:
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

        flip_x = AppState.get_attr("flip_x")
        flip_y = AppState.get_attr("flip_y")
        sigma = AppState.get_attr("noise_sigma")
        spatial_size = MoveNet.INPUT_SIZE.value
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

        X = np.array(X)
        y = np.array(y)
        X_copy = X.copy()
        y_copy = y.copy()

        if flip_x:
            mask_x = np.tile([True, False], spatial_size//2)
            flipped_x = X_copy.copy()
            flipped_x[..., mask_x] = -flipped_x[..., mask_x]
            X = np.concatenate([X, flipped_x], axis=0)
            y = np.concatenate([y, y_copy], axis=0)
            AppState.train_log(f"Data augmentation: mirroring on X-axis")

        if flip_y:
            mask_y = np.tile([False, True], spatial_size//2)
            flipped_y = X_copy.copy()
            flipped_y[..., mask_y] = -flipped_y[..., mask_y]
            X = np.concatenate([X, flipped_y], axis=0)
            y = np.concatenate([y, y_copy], axis=0)
            AppState.train_log(f"Data augmentation: mirroring on Y-axis")

        if sigma > 0.0:
            noise = sigma*np.random.normal(loc=0.0, scale=1, size=X.shape)
            X = np.concatenate([X, noise+X], axis=0)
            y = np.concatenate([y, y], axis=0)
            AppState.train_log(f"Data augmentation: Appending noisy(Gaussian white noise, std dev={sigma}) copy of original dataset.")
 
        X = np.expand_dims(X, -1)
        y = np.expand_dims(y, -1)

        AppState.train_log(f"Dataset Shape: {X.shape}")

        if test_split > 0.0:
            AppState.train_log(f"Splitting datasets: test split={test_split}")
            X_trn, X_val, y_trn, y_val = train_test_split(X, y, test_size=test_split)
            print(X_trn.shape)
            AppState.train_log("Preprocessing Complete")
            return tf.convert_to_tensor(X_trn), tf.convert_to_tensor(y_trn), tf.convert_to_tensor(X_val), tf.convert_to_tensor(y_val), label_map
        else:
            AppState.train_log("Preprocessing Complete")
            return tf.convert_to_tensor(X), tf.convert_to_tensor(y), None, None, label_map
