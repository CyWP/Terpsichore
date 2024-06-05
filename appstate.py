import json
from os import path, makedirs, listdir, remove
import subprocess
import webbrowser
import shutil
from model import Model
from terpsexception import TerpsException, InvalidModelException
from customtkinter import filedialog

class AppState:
    _state_file = None
    _state_dict = None
    _ui_input_state = None
    _models_dir = None
    _active_model = None
    _state = None
    _training = False
    _training_logs = []
    _stop_training = False
    _cancel_training = False
    _file_records = []
    _abort_engine = False
    _learn_rates = [0.001, 0.005, 0.01, 0.05, 0.1]

    @classmethod
    def set_root(cls, filepath):
        cls._root = filepath
        if not path.exists(filepath):
            makedirs(filepath)
        cls._models_dir = path.join(filepath, "Models")
        if not path.exists(cls._models_dir):
            makedirs(cls._models_dir)
        cls._del_dir = path.join(filepath, "Deleted")
        if not path.exists(cls._del_dir):
            makedirs(cls._del_dir)

    @classmethod
    def load_state(cls, filepath):
        cls._state_file = filepath
        if not path.exists(cls._state_file):
            cls.default_state()
        else:
            with open(filepath, "r") as f:
                cls._state_dict = json.load(f)
        cls.set_root(cls._state_dict["data"])
        cls.load_last_model()

    @classmethod
    def close(cls):
        cls.save_ui_state()
        cls.clear_deleted()

    @classmethod
    def start_engine(cls):
        cls.abort_engine = False

    @classmethod
    def abort_engine(cls):
        cls._abort_engine = True

    @classmethod
    def engine_aborted(cls):
        ret = cls._abort_engine
        cls._abort_engine = False
        return ret

    @classmethod
    def check_active_model(cls):
        if cls._active_model is None or cls._state_dict["active_model"] is None:
            raise TerpsException("Error: no model currently active/selected.")

    @classmethod
    def active_model(cls):
        cls.check_active_model()
        return cls._active_model

    @classmethod
    def save_ui_state(cls):
        with open(cls._state_file, "w") as f:
            json.dump(cls._state_dict, f, indent=4)

    @classmethod
    def clear_deleted(cls):
        shutil.rmtree(cls._del_dir)

    @classmethod
    def get_models(cls):
        return [
            name
            for name in listdir(cls._models_dir)
            if path.isdir(path.join(cls._models_dir, name))
        ]

    @classmethod
    def active_model_info(cls):
        if cls._active_model is not None:
            return cls._active_model.get_info()
        else:
            return None

    @classmethod
    def load_model(cls, name: str):
        prev_model = cls._active_model
        prev_name = cls._state_dict["active_model"]
        if name in cls.get_models():
            cls._active_model = Model(cls._models_dir, name, new=False)
            cls._state_dict["active_model"] = name
        if not path.exists(path.join(cls._models_dir, name)):
            cls._active_model = prev_model
            cls._state_dict["active_model"] = prev_name

    @classmethod
    def load_last_model(cls):
        if cls._state_dict["active_model"] in cls.get_models():
            cls.load_model(cls._state_dict["active_model"])
        else:
            cls._state_dict["active_model"] = None

    @classmethod
    def get_model_checkpoint(cls):
        if cls._active_model is not None:
            return cls._active_model.get_checkpoint_path()

    @classmethod
    def get_model_dir(cls):
        if cls._active_model is not None:
            return cls._active_model.path

    @classmethod
    def get_gesture_paths(cls):
        if cls._active_model is not None:
            return cls._active_model.gesture_paths()

    @classmethod
    def get_num_classes(cls):
        if cls._active_model is not None:
            return cls._active_model.num_gestures()

    @classmethod
    def save_model(cls):
        cls._active_model.save()

    @classmethod
    def save_model_as(cls, name: str):
        if name not in cls._models.keys():
            cls._active_model.save_as(name)

    @classmethod
    def new_model(cls, name: str):
        if name.strip() == "":
            raise TerpsException("Error: Cannot create unnamed model. Provide a valid name in entry.")
        if name not in cls.get_models():
            cls._active_model = Model(cls._models_dir, name, new=True)
            cls._state_dict["active_model"] = name
        else:
            cls.load_model(name)
            raise TerpsException(f"Error: Model {name} already exists and was loaded instead.")

    @classmethod
    def delete_model(cls, name=None):
        if name is None:
            name = cls._state_dict["active_model"]
        if name is None:
            raise TerpsException(f"Error: no currently active model.")
        if name not in cls.get_models():
            raise TerpsException(f"Error: {name} is not an existing model name.")
        cls.load_model(name)
        model = cls._active_model
        shutil.move(
            model.path, path.join(cls._del_dir, cls._state_dict["active_model"])
        )
        if len(cls.get_models()) > 0:
            cls.load_model(cls.get_models()[-1])
        else:
            cls._active_model = None
            cls._state_dict["active_model"] = None

    @classmethod
    def export_active_model(cls):
        cls.check_active_model()
        dirpath = filedialog.askdirectory(
            initialdir="/", title="Select Folder", mustexist=True
        )
        cls.active_model().export(dirpath)

    @classmethod
    def import_model(cls, name:str):
        filename = filedialog.askopenfilename(
            defaultextension=".tar.gz", initialdir="/"
        )
        if name.strip() == "":
            name = path.basename(filename[:-7])
        if name not in cls.get_models():
            try:
                cls._active_model = Model(
                    cls._models_dir, name, new=False, tarpath=filename
                )
            except Exception as e:
                raise TerpsException(
                    f"An error occured while loading {filename}, imported file might be invalid: {str(e)}"
                )
            cls._state_dict["active_model"] = name
        else:
            # Should probably add some error handling for if folder is created but not model object.
            raise TerpsException(
                f"Model {name} already exists. Specify another name for the model you wish to import."
            )

    @classmethod
    def restore_deleted(cls):
        dirs = listdir(cls._del_dir)
        if len(dirs) > 0:
            for dir in dirs:
                shutil.move(
                    path.join(cls._del_dir, dir), path.join(cls._models_dir, dir)
                )
            cls.load_model(dirs[-1])
        else:
            raise TerpsException("Error: No model to restore.")

    @classmethod
    def copy_model(cls, name):
        if (
            None not in (cls._active_model, cls._state_dict["active_model"])
            and name != ""
        ):
            shutil.copytree(cls._active_model.path, path.join(cls._models_dir, name))
            cls.load_model(name)

    @classmethod
    def new_gesture(cls, name: str):
        if cls._active_model is not None:
            cls._active_model.add_gesture(name)

    @classmethod
    def remove_gesture(cls, name: str):
        if cls._active_model is not None:
            cls._active_model.remove_gesture(name)

    @classmethod
    def select_gesture(cls, name: str):
        if cls._active_model is not None:
            if cls._active_model.select_gesture(name):
                cls._state_dict["active_gesture"] = name

    @classmethod
    def get_gestures(cls):
        try:
            ret = cls._active_model.get_gestures()
        except:
            ret = []
        return ret

    @classmethod
    def get_active_gesture(cls):
        if cls._active_model is not None:
            return cls._active_model.active_gesture
        return ""

    @classmethod
    def set_ui_state(cls, dict):
        cls._state_dict.update(dict)

    @classmethod
    def update_state(cls, state: dict):
        cls._state_dict.update(state)

    @classmethod
    def get_attr(cls, attr: str):
        try:
            return cls._state_dict[attr]
        except:
            raise TerpsException(f"Attribute {attr} invalid or uninitialized.")

    @classmethod
    def get_csv_file(cls):
        if cls._active_model is not None:
            rec = cls._active_model.get_csv_file()
            cls._file_records.append(rec)
            return rec

    @classmethod
    def undo_last_rec(cls):
        if len(cls._file_records):
            remove(cls._file_records.pop())

    @classmethod
    def start_train(cls):
        cls._training = True

    @classmethod
    def end_train(cls):
        cls._training = False

    @classmethod
    def train_log(cls, log):
        print(log)
        cls._training_logs.append(log)

    @classmethod
    def get_trained_info(cls):
        if cls._active_model is not None:
            return cls._active_model.get_training_info()

    @classmethod
    def get_train_logs(cls):
        temp = cls._training_logs
        cls._training_logs = []
        return temp

    @classmethod
    def is_trained(cls):
        if cls._active_model is not None:
            return cls._active_model.is_trained()
        return False
    
    @classmethod
    def cancel_training(cls):
        cls._cancel_training = True

    @classmethod
    def stop_training(cls):
        cls._stop_training = True
    
    @classmethod
    def reset_training(cls):
        cls._training = False
        cls._training_logs = []
        cls._stop_training = False
        cls._cancel_training = False

    @classmethod
    def update_model(cls, label_map: dict):
        if cls._active_model is not None:
            cls._active_model.update_model_info(label_map)

    @classmethod
    def open_models_folder(cls):
        try:
            subprocess.Popen(f'explorer "{cls._models_dir}"')
        except:
            try:
                subprocess.Popen(["open", cls._models_dir])
            except:
                try:
                    subprocess.Popen(["xdg-open", cls._models_dir])
                except:
                    raise TerpsException("What the fuck are you running? FreeBSD?")

    @classmethod
    def open_github(cls):
        webbrowser.open_new("https://github.com/CyWP/Terpsichore")

    @classmethod
    def default_state(cls):
        cls._state_dict = {
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
            "epochs": 50,
            "batch_size": 32,
            "learn_rate": 0.05,
            "augment": False,
            "flip_x": False,
            "flip_y": False,
            "noise": False,
            "noise_sigma": 0.02,
            "test_split": 15.0,
            "learn_rate": 0.05,
            "temporal_size": 34,
            "regularization": True,
            "data": path.join(path.expanduser("~"), ".terpsichore"),
            "active_model": "",
        }