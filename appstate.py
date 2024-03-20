import json
from os import path, makedirs, listdir
from model import Model
class AppState:
    _state_file = None
    _state_dict = None
    _ui_input_state = None
    _models_dir = None
    _models = {}
    _last_model = None
    _active_model = None
    _state = None

    _classification_outputs = ['Integer', 'Softmax', 'One Hot']

    @classmethod
    def set_root(_cls, filepath):
        if not path.exists(filepath):
            makedirs(filepath)
        _cls.models_dir = path.join(filepath, 'Models')
        if not path.exists(_cls.models_dir):
            makedirs(_cls.models_dir)

    @classmethod
    def load_state(_cls, filepath):
        _cls._state_file = filepath
        if not path.exists(_cls._state_file):
            print('ho')
            _cls.default_state()
        else:
            print('ha')
            with open(filepath, 'r') as f:
                _cls._state_dict = json.load(f)
        _cls.set_root(_cls._state_dict['data'])
        _cls.get_models

    @classmethod
    def save_ui_state(_cls):
        print(_cls._state_dict.values())
        with open(_cls._state_file, 'w') as f:
            json.dump(_cls._state_dict, f, indent=4)

    @classmethod
    def get_models(_cls):
        for name in listdir(_cls._models_dir):
            if path.isdir(path.join(_cls._models_dir, name)):
                _cls._models[name] = Model(_cls.models_dir, name, new=False)

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
    def update_ui_inputs(_cls):
        _cls.get_ui_inputs()

    @classmethod
    def update_state(_cls, state: dict):
        _cls._state_dict.update(state)

    @classmethod
    def get_attr(_cls, attr:str):
        try:
            return _cls._state_dict[attr]
        except:
            print(f'Attribute {attr} is invalid.')

    @classmethod
    def default_state(_cls):
        _cls._state_dict = {
                    'webcam_active': True,
                    'webcam_index': 0,
                    'delay': 0,
                    'duration': 10,
                    'video_path': '/path/to/video',
                    'class_output': 'Integer',
                    'send_pose': True,
                    'show': True,
                    'show_pose': True,
                    'osc_port': 2442,
                    'max_frequency': 0,
                    'epochs': 50,
                    'target_loss': 0.,
                    'test_split': 0.15,
                    'cuda': True,
                    'regularization': True,
                    'data': path.join(path.expanduser('~'), 'Documents', 'Terpsichore_Data'),
                    'active_model': ''
                    }