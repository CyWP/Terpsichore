from appstate import AppState
import tensorflow as tf
from .mvnet import MoveNet


class TrainingCallback(tf.keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        AppState.train_log(
            f"Epoch {epoch+1}, Loss: {logs['loss']}, Accuracy: {logs['accuracy']}"
        )

    def on_train_begin(self, logs=None):
        AppState.start_train()
        AppState.train_log("Training begins")
        AppState.train_log(logs)

    def on_train_end(self, logs=None):
        AppState.train_log(logs)
        AppState.train_log("End of training")


class ShallowCNN(tf.keras.Model):
    """
    Subclass of tf.keras.Model for building and training shallow Convolutional Neural Network (CNN) models.
    """

    def __init__(self, input_shape, num_classes):
        """
        Initializes the ShallowCNN model.

        Args:
            input_shape (tuple): The input shape of the model.
            num_classes (int): The number of classes for classification.
        """
        super(ShallowCNN, self).__init__()
        self.custom_input_shape = input_shape
        self.num_classes = num_classes
        self.build_model()
        self.compile_model()

    def build_model(self):
        """
        Builds the shallow CNN classification model.

        Returns:
            None
        """
        self.model = tf.keras.Sequential()

        # Convolutional layers with L2 regularization
        self.model.add(
            tf.keras.layers.Conv1D(
                32,
                kernel_size=3,
                activation="relu",
                input_shape=self.custom_input_shape,
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(tf.keras.layers.MaxPooling1D(pool_size=2))

        self.model.add(
            tf.keras.layers.Conv1D(
                64,
                kernel_size=3,
                activation="relu",
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(tf.keras.layers.MaxPooling1D(pool_size=2))

        # Adding another convolutional layer with L2 regularization
        self.model.add(
            tf.keras.layers.Conv1D(
                128,
                kernel_size=3,
                activation="relu",
                padding="same",
                kernel_regularizer=tf.keras.regularizers.l2(0.01),
            )
        )
        self.model.add(tf.keras.layers.MaxPooling1D(pool_size=2))

        # Flatten the feature maps
        self.model.add(tf.keras.layers.Flatten())

        # Dense layers
        self.model.add(tf.keras.layers.Dense(128, activation="relu"))
        self.model.add(tf.keras.layers.Dense(self.num_classes, activation="softmax"))

    def compile_model(self):
        """
        Compiles the classification model.
        """
        self.model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

    def call(self, inputs):
        """
        Forward pass of the model.

        Args:
            inputs (tensor): Input tensor to the model.

        Returns:
            tensor: Output tensor from the model.
        """
        return self.model(inputs)

    def train(self, X_trn, y_trn):
        """
        Trains the classification model.

        Args:
            x_train (numpy.ndarray): Training input data.
            y_train (numpy.ndarray): Training labels.
            epochs (int): Number of epochs for training.
            batch_size (int): Batch size for training.
        """
        epochs = AppState.get_attr("epochs")

        batch_size = 32

        self.model.fit(
            x=X_trn,
            y=y_trn,
            batch_size=batch_size,
            epochs=epochs,
            callbacks=[TrainingCallback()],
        )

    def evaluate(self, x_test, y_test):
        """
        Evaluates the classification model.

        Args:
            x_test (numpy.ndarray): Test input data.
            y_test (numpy.ndarray): Test labels.

        Returns:
            list: Evaluation results.
        """
        return self.model.evaluate(x_test, y_test)

    def save(self, filepath):
        """
        Saves the weights of the classification model to a file.

        Args:
            filepath (str): Filepath to save the weights.
        """
        self.model.save(filepath)


def get_classifier(name=""):
    """
    Factory function to get a classifier based on the specified name.

    Args:
        name (str): Name of the classifier.

    Returns:
        Classifier: Instance of the specified classifier.
    """
    input_shape = (MoveNet.TEMPORAL_AXIS_SIZE.value, MoveNet.INPUT_SIZE.value)

    num_classes = AppState.get_num_classes()

    return ShallowCNN(input_shape, num_classes)
