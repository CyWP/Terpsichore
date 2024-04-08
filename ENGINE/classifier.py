from appstate import AppState
import tensorflow as tf
from keras import layers, models, regularizers, callbacks, Model

class TrainingCallback(callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        AppState.train_log(f"Epoch {epoch+1}, Loss: {logs['loss']}, Accuracy: {logs['accuracy']}")

    def on_train_begin(self, logs=None):
        AppState.start_train()
        AppState.train_log("Training begins")

    def on_train_end(self, logs=None):
        AppState.end_train()
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
        self.input_shape = input_shape
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
        self.model.add(layers.Conv1D(32, kernel_size=3, activation='relu', input_shape=self.input_shape, padding='same', kernel_regularizer=regularizers.l2(0.01)))
        self.model.add(layers.MaxPooling1D(pool_size=2))
        
        self.model.add(layers.Conv1D(64, kernel_size=3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)))
        self.model.add(layers.MaxPooling1D(pool_size=2))

        # Adding another convolutional layer with L2 regularization
        self.model.add(layers.Conv1D(128, kernel_size=3, activation='relu', padding='same', kernel_regularizer=regularizers.l2(0.01)))
        self.model.add(layers.MaxPooling1D(pool_size=2))

        # Flatten the feature maps
        self.model.add(layers.Flatten())

        # Dense layers
        self.model.add(layers.Dense(128, activation='relu'))
        self.model.add(layers.Dense(self.num_classes, activation='softmax'))


    def compile_model(self):
        """
        Compiles the classification model.
        """
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    def call(self, inputs):
        """
        Forward pass of the model.

        Args:
            inputs (tensor): Input tensor to the model.

        Returns:
            tensor: Output tensor from the model.
        """
        return self.model(inputs)
    
    def train(self, x_train, y_train, x_val, y_val, epochs=10, batch_size=32):
        """
        Trains the classification model.

        Args:
            x_train (numpy.ndarray): Training input data.
            y_train (numpy.ndarray): Training labels.
            x_val (numpy.ndarray): Validation input data.
            y_val (numpy.ndarray): Validation labels.
            epochs (int): Number of epochs for training.
            batch_size (int): Batch size for training.
        """
        self.model.fit(x_train, y_train,
                       batch_size=batch_size,
                       epochs=epochs,
                       validation_data=(x_val, y_val),
                       callbacks=[TrainingCallback()])
        
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
    
    def save_weights(self, filepath):
        """
        Saves the weights of the classification model to a file.

        Args:
            filepath (str): Filepath to save the weights.
        """
        self.model.save_weights(filepath)

    def load_weights(self, filepath):
        """
        Loads the weights of the classification model from a file.

        Args:
            filepath (str): Filepath to load the weights from.
        """
        self.model.load_weights(filepath)


def get_classifier(name: str):
    """
    Factory function to get a classifier based on the specified name.

    Args:
        name (str): Name of the classifier.

    Returns:
        Classifier: Instance of the specified classifier.
    """
    return ShallowCNN()