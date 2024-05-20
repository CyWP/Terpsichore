import json
from os import path, makedirs, listdir, remove
import subprocess
import webbrowser
import shutil
from model import Model
from terpsexception import TerpsException
from customtkinter import filedialog
import asyncio


class AppState:
    _state_file = None
    _state_dict = None
    _ui_input_state = None
    _models_dir = None
    _active_model = None
    _state = None
    _training = False
    _training_logs = []
    _file_records = []
    _abort_engine = False
    _classification_outputs = ["Integer", "Softmax", "One Hot"]

    @classmethod
    def set_root(_cls, filepath):
        _cls._root = filepath
        if not path.exists(filepath):
            makedirs(filepath)
        _cls._models_dir = path.join(filepath, "Models")
        if not path.exists(_cls._models_dir):
            makedirs(_cls._models_dir)
        _cls._del_dir = path.join(filepath, "Deleted")
        if not path.exists(_cls._del_dir):
            makedirs(_cls._del_dir)

    @classmethod
    def load_state(_cls, filepath):
        _cls._state_file = filepath
        if not path.exists(_cls._state_file):
            _cls.default_state()
        else:
            with open(filepath, "r") as f:
                _cls._state_dict = json.load(f)
        _cls.set_root(_cls._state_dict["data"])
        _cls.load_last_model()

    @classmethod
    def close(_cls):
        _cls.save_ui_state()
        _cls.clear_deleted()

    @classmethod
    def start_engine(_cls):
        _cls.abort_engine = False

    @classmethod
    def abort_engine(_cls):
        _cls._abort_engine = True

    @classmethod
    def engine_aborted(_cls):
        ret = _cls._abort_engine
        _cls._abort_engine = False
        return ret

    @classmethod
    def check_active_model(_cls):
        if _cls._active_model is None or _cls._state_dict["active_model"] is None:
            raise TerpsException("Error: no model currently active/selected.")

    @classmethod
    def active_model(_cls):
        _cls.check_active_model()
        return _cls._state_dict["active_model"]

    @classmethod
    def save_ui_state(_cls):
        with open(_cls._state_file, "w") as f:
            json.dump(_cls._state_dict, f, indent=4)

    @classmethod
    def clear_deleted(_cls):
        shutil.rmtree(_cls._del_dir)

    @classmethod
    def get_models(_cls):
        return [
            name
            for name in listdir(_cls._models_dir)
            if path.isdir(path.join(_cls._models_dir, name))
        ]

    @classmethod
    def active_model_info(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.get_info()
        else:
            return None

    @classmethod
    def load_model(_cls, name: str):
        if name in _cls.get_models():
            _cls._active_model = Model(_cls._models_dir, name, new=False)
            _cls._state_dict["active_model"] = name

    @classmethod
    def load_last_model(_cls):
        if _cls._state_dict["active_model"] in _cls.get_models():
            _cls.load_model(_cls._state_dict["active_model"])
        else:
            _cls._state_dict["active_model"] = None

    @classmethod
    def get_model_checkpoint(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.get_checkpoint_path()

    @classmethod
    def get_model_dir(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.path

    @classmethod
    def get_gesture_paths(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.gesture_paths()

    @classmethod
    def get_num_classes(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.num_gestures()

    @classmethod
    def save_model(_cls):
        _cls._active_model.save()

    @classmethod
    def save_model_as(_cls, name: str):
        if name not in _cls._models.keys():
            _cls._active_model.save_as(name)

    @classmethod
    def new_model(_cls, name: str):
        if name not in _cls.get_models():
            _cls._active_model = Model(_cls._models_dir, name, new=True)
            _cls._state_dict["active_model"] = name
        else:
            _cls.load_model(name)
            raise TerpsException(f"Model {name} already exists and was loaded instead.")

    @classmethod
    def delete_model(_cls, name=None):

        if name not in _cls.get_models():
            raise TerpsException(f"Error: {name} is not an existing model name.")
        _cls.load_model(name)
        model = _cls._active_model
        shutil.move(
            model.path, path.join(_cls._del_dir, _cls._state_dict["active_model"])
        )
        if len(_cls.get_models()) > 0:
            _cls.load_model(_cls.get_models()[-1])
        else:
            _cls._active_model = None
            _cls._state_dict["active_model"] = None

    @classmethod
    def export_model(_cls):
        _cls.check_active_model()
        dirpath = filedialog.askdirectory(
            initialdir="/", title="Select Folder", mustexist=True
        )
        _cls.active_model().export(dirpath)

    @classmethod
    def import_model(_cls):
        filename = filedialog.askopenfilename(
            defaultextension=".tar.gz", initialdir="/"
        )
        name = filename[:-7]
        if name not in _cls.get_models():
            try:
                _cls._active_model = Model(
                    _cls._models_dir, name, new=True, tarpath=filename
                )
            except Exception as e:
                raise TerpsException(
                    f"An error occured while loading {filename}, imported file might be invalid: {str(e)}"
                )
            _cls._state_dict["active_model"] = name
        else:
            # Should probably add some error handling for if folder is created but not model object.
            raise TerpsException(
                f"Model {name} already exists. Change the name of file you wish to load."
            )

    @classmethod
    def restore_deleted(_cls):
        dirs = listdir(_cls._del_dir)
        if len(dirs) > 0:
            for dir in dirs:
                shutil.move(
                    path.join(_cls._del_dir, dir), path.join(_cls._models_dir, dir)
                )
            _cls.load_model(dirs[-1])
        else:
            raise TerpsException("Error: No model to restore.")

    @classmethod
    def copy_model(_cls, name):
        if (
            None not in (_cls._active_model, _cls._state_dict["active_model"])
            and name != ""
        ):
            shutil.copytree(_cls._active_model.path, path.join(_cls._models_dir, name))
            _cls.load_model(name)

    @classmethod
    def new_gesture(_cls, name: str):
        if _cls._active_model is not None:
            _cls._active_model.add_gesture(name)

    @classmethod
    def remove_gesture(_cls, name: str):
        if _cls._active_model is not None:
            _cls._active_model.remove_gesture(name)

    @classmethod
    def select_gesture(_cls, name: str):
        if _cls._active_model is not None:
            if _cls._active_model.select_gesture(name):
                _cls._state_dict["active_gesture"] = name

    @classmethod
    def get_gestures(_cls):
        try:
            ret = _cls._active_model.get_gestures()
        except:
            ret = []
        return ret

    @classmethod
    def get_active_gesture(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.active_gesture
        return ""

    @classmethod
    def set_ui_state(_cls, dict):
        _cls._state_dict.update(dict)

    @classmethod
    def update_state(_cls, state: dict):
        _cls._state_dict.update(state)

    @classmethod
    def get_attr(_cls, attr: str):
        try:
            return _cls._state_dict[attr]
        except:
            raise TerpsException(f"Attribute {attr} invalid or uninitialized.")

    @classmethod
    def get_csv_file(_cls):
        if _cls._active_model is not None:
            rec = _cls._active_model.get_csv_file()
            _cls._file_records.append(rec)
            return rec

    @classmethod
    def undo_last_rec(_cls):
        if len(_cls._file_records):
            remove(_cls._file_records.pop())

    @classmethod
    def start_train(_cls):
        _cls._training = True

    @classmethod
    def end_train(_cls):
        _cls._training = False

    @classmethod
    def train_log(_cls, log):
        print(log)
        _cls._training_logs.append(log)

    @classmethod
    def get_trained_info(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.get_training_info()

    @classmethod
    def get_train_logs(_cls):
        temp = _cls._training_logs
        _cls._training_logs = []
        return temp

    @classmethod
    def is_trained(_cls):
        if _cls._active_model is not None:
            return _cls._active_model.is_trained()
        return False

    @classmethod
    def update_model(_cls, label_map: dict):
        if _cls._active_model is not None:
            _cls._active_model.update_model_info(label_map)

    @classmethod
    def open_folder(_cls):
        try:
            subprocess.Popen(f'explorer "{_cls._root}"')
        except:
            try:
                subprocess.Popen(["open", _cls._root])
            except:
                try:
                    subprocess.Popen(["xdg-open", _cls._root])
                except:
                    raise TerpsException("What the fuck are you running? FreeBSD?")

    @classmethod
    def open_github(_cls):
        webbrowser.open_new("https://github.com/CyWP/Terpsichore")

    @classmethod
    def default_state(_cls):
        _cls._state_dict = {
            "webcam_active": True,
            "webcam_index": 0,
            "delay": 0,
            "duration": 10,
            "video_path": "/path/to/video",
            "class_output": "Integer",
            "send_pose": True,
            "show": True,
            "show_pose": True,
            "osc_ip": "127.0.0.1",
            "osc_port": 2442,
            "listen_port": 2443,
            "osc_address": "/terp",
            "momentum": 0.2,
            "conf_threshold": 0.07,
            "x_loc": 50.0,
            "y_loc": 50.0,
            "custom_size": False,
            "x_size": 50.0,
            "y_size": 50.0,
            "max_frequency": 0,
            "epochs": 50,
            "target_loss": 0.0,
            "test_split": 15.0,
            "cuda": True,
            "regularization": True,
            "data": path.join(path.expanduser("~"), ".terpsichore"),
            "active_model": "",
        }
