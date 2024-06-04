from appstate import AppState
import tensorflow as tf
import logging
from .mvnet import MoveNet
from terpsexception import TerpsException

class TrainingCallback(tf.keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        AppState.train_log(
            f"Epoch {epoch+1}, Loss: {logs['loss']}, Accuracy: {logs['accuracy']}"
        )

    def on_batch_end(self, batch, logs=None):
        if AppState._stop_training:
            self.model.stop_training = True
            AppState.train_log("Training stopped manually.") 
        if AppState._cancel_training:
            self.model.stop_training = True
            AppState.train_log("Training aborted. Model will not be saved.")
        
    def on_train_begin(self, logs=None):
        AppState.start_train()
        AppState.train_log("Training begins")
        AppState.train_log(logs)

    def on_train_end(self, logs=None):
        AppState.train_log(logs)
        AppState.train_log("End of training")

class Classifier(tf.keras.Model):

    def __init__(self):
        super(Classifier, self).__init__()
        try:
            self.temporal_size = int(AppState.get_attr("temporal_size"))
            self.batch_size = int(AppState.get_attr("batch_size"))
        except:
            raise TerpsException("Error: Invalid UI input.")
        tf.get_logger().setLevel(logging.ERROR)
        self.spatial_size = MoveNet.INPUT_SIZE.value
        self.custom_input_shape = (self.temporal_size, self.spatial_size, 1)
        self.num_classes = AppState.get_num_classes()
        self.build_model()
        self.compile_model()

    def build_model(self):
        self.model = None
        pass

    def compile_model(self):
        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

    def call(self):
        pass

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)
    
    def train(self, X_trn, y_trn, X_val, y_val):
        try:
            epochs = AppState.get_attr("epochs")
            batch_size = AppState.get_attr("batch_size")
        except:
            raise TerpsException("Error: Invalid UI input.")

        self.model.fit(
            x=X_trn,
            y=y_trn,
            batch_size=batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val),
            callbacks=[TrainingCallback()],
        )

    def save(self, filepath):
        self.model.save(filepath)

class ShallowCNN(Classifier):

    def build_model(self):
        self.model = tf.keras.Sequential()

        self.model.add(
            tf.keras.layers.Conv2D(
                32,
                kernel_size=(self.temporal_size//3, 1),
                activation="relu",
                input_shape=self.custom_input_shape,
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(
            tf.keras.layers.Conv2D(
                64,
                kernel_size=(1, self.spatial_size),
                activation="relu",
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(
            tf.keras.layers.Conv2D(
                32,
                kernel_size=(1, 1),
                activation="relu",
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(tf.keras.layers.MaxPooling2D(pool_size=2))
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dense(self.num_classes, activation="softmax"))

def get_classifier(name=""):

    return ShallowCNN()
