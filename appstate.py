from UI.app import App
import json
from os import path, makedirs
from UI.customclasses import Log

class AppState:
    _state_file = None
    _models = None
    _active_model = None
    _app = None
    _statefile = None
    _state = None

    @classmethod
    def set_root(_cls, filepath):
        _root = filepath
        if not path.exists(_root):
            makedirs(_root)
        if not path.exists(path.join(_root, 'Models')):
            makedirs(path.join(_root, 'Models'))

    @classmethod
    def load(_cls, filepath):
        _state_file = filepath

    @classmethod
    def set_app(_cls, app:App):
        _cls._app = app

    @classmethod
    def set_app_title(_cls, title:str):
        _cls.app.title(title)

    @classmethod
    def get_models(_cls):
        pass

    @classmethod
    def load_model(_cls, name:str):
        pass
    
    @classmethod
    def save_model(_cls):
        pass

    @classmethod
    def save_model_as(_cls, name:str):
        pass

    @classmethod
    def new_model(_cls, name:str):
        pass

    @classmethod
    def get_ui_inputs(_cls):

        win = _cls._app.body
        return {'use_webcam': win.webcam_active.get(),
                'webcam_index': int(win.webcam_index.get()),
                'delay': int(win.input_delay.get()),
                'duration': int(win.input_duration.get()),
                'video_path': win.video_path.get(),
                'class_output': win.classification_output.get(),
                'send_pose': win.send_pose_data.get(),
                'show': win.display_input.get(),
                'show_pose': win.display_pose.get(),
                'osc_port': int(win.osc_port.get()),
                'max_frequency': int(win.max_freq.get()),
                'epochs': int(win.train_epochs.get()),
                'target_loss': float(win.target_loss.get()),
                'test_split': float(win.test_split.get()),
                'cuda': win.use_cuda.get(),
                'regularization': win.use_regularization.get()}
    
    @classmethod
    def log(_cls, log):
        _cls.app.log.configure(text=str(log))