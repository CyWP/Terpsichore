import json
from os import path, remove, listdir, mkdir
import time
import copy
import shutil
import tarfile
from terpsexception import TerpsException, InvalidModelException


class Model:

    def __init__(self, dirpath, name, new: bool, tarpath=None):
        self.path = path.join(dirpath, name)
        self.root = dirpath
        self.gestures = {}
        self.gestures_dir = path.join(self.path, "gestures")
        if tarpath is not None:
            if tarpath[-7:] != ".tar.gz":
                raise TerpsException(
                    "Error: Improper file type imported, must be tarball (.tar.gz)."
                )
            with tarfile.open(tarpath, "r:gz") as tar:
                if tar.getmembers()[0].name != name:
                    replace = tar.getmembers()[0].name
                    for member in tar.getmembers():
                        member.name = name+member.name[len(replace):]
                tar.extractall(path.dirname(tarpath))            
            shutil.move(path.join(path.dirname(tarpath), name), dirpath)
        self.info_path = path.join(self.path, "info.json")
        self.ckptname = "checkpoint"
        self.checkpoint = path.join(dirpath, self.ckptname)
        self.name = name
        self.active_gesture = None

        if new or not path.exists(self.path):
            self.create()
        else:
            self.load()

    def load(self):
        try:
            with open(self.info_path, "r") as f:
                self.info = json.load(f)
        except:
            raise InvalidModelException(f"Model {self.name} could not be loaded. Check its file structure.", self.path)
        for gesture in self.get_gesture_names():
            self.gestures[gesture] = Gesture(path.join(self.gestures_dir, gesture), new=False)
        if len(self.gestures.keys()):
            self.select_gesture(list(self.gestures.keys())[0])

    def create(self):
        self.info = Model.default_info()
        try:
            mkdir(self.path)
        except Exception as e:
            raise TerpsException(f"Error occured while creating Model: {str(e)}")

    def export(self, dirpath):
        with tarfile.open(path.join(dirpath, f"{self.name}.tar.gz"), "w:gz") as tar:
            tar.add(self.path, arcname=path.basename(self.path))

    def add_gesture(self, name):
        if not path.exists(path.join(self.gestures_dir, name)):
            self.gestures[name] = Gesture(path.join(self.gestures_dir, name), new=True)
            self.select_gesture(name)

    def remove_gesture(self, name):
        try:
            self.gestures[name].erase_all()
            self.gestures.pop(name)
            if self.active_gesture == name:
                if len(self.gestures.keys()):
                    self.select_gesture(list(self.gestures.keys())[0])
        except Exception as e:
            raise TerpsException(f"An error occured while deleting the model: {str(e)}")

    def select_gesture(self, name):
        if name in self.gestures.keys():
            self.active_gesture = name

    def get_gestures(self):
        return [
            (name, str(gesture.get_recs()), f"{gesture.get_space()/1000:.1f}kB")
            for name, gesture in self.gestures.items()
        ]

    def gesture_paths(self):
        return [(name, gesture.path) for name, gesture in self.gestures.items()]

    def num_gestures(self):
        return len(self.gestures.items())

    def gesture_space(self):
        return f"{sum([gesture.get_space() for name, gesture in self.gestures.items()])/1000}kB"

    def get_gesture_names(self):
        return [
            gesture
            for gesture in listdir(self.gestures_dir)
            if gesture != self.ckptname and path.isdir(path.join(self.gestures_dir, gesture))
        ]

    @classmethod
    def default_info(_cls):
        return {"trained": False, "gestures": {}}

    def save(self):
        with open(self.info_path, "w") as f:
            json.dump(self.info, f, indent=4)

    def save_as(self, name):
        self.path = path.join(self.root, name)
        mkdir(self.path)
        for gesture in self.gestures:
            gesture = copy.deepcopy(gesture)
            gesture.rebase(path.join(self.gestures_dir, gesture))
        self.save()

    def is_trained(self):
        return self.info["trained"]

    def get_info(self):
        return [
            ("Name", self.name),
            ("Path", self.path),
            ("Gestures", len(self.gestures.keys())),
            ("Space", self.gesture_space()),
            ("Is trained", str(self.is_trained())),
        ]

    def get_training_info(self):
        return [(gesture, label) for gesture, label in self.info["gestures"].items()]

    def get_csv_file(self):
        if self.active_gesture is not None:
            return path.join(
                self.path, self.active_gesture, f"{int(time.time()*10)}.csv"
            )

    def get_checkpoint_path(self):
        return self.checkpoint

    def update_model_info(self, label_map: dict):
        self.info["trained"] = True
        self.info["gestures"] = label_map
        self.save()

class Gesture:

    def __init__(self, dirpath, new: bool):
        self.path = dirpath
        self.last_rec = None
        self.space = 0
        self.recs = 0
        if new or not path.exists(self.path):
            self.create()
        else:
            self.load()

    def create(self):
        mkdir(self.path)

    def load(self):
        for file in listdir(self.path):
            if path.isfile(path.join(self.path, file)):
                self.recs += 1
                self.space += path.getsize(path.join(self.path, file))

    def get_recording_file(self):
        self.last_rec = path.join(self.path, str(int(time.time())))
        return self.last_rec

    def get_recs(self):
        self.recs = 0
        for file in listdir(self.path):
            if path.isfile(path.join(self.path, file)):
                self.recs += 1
        return self.recs

    def get_space(self):
        self.space = 0
        for file in listdir(self.path):
            if path.isfile(path.join(self.path, file)):
                self.space += path.getsize(path.join(self.path, file))
        return self.space

    def delete_last_rec(self):
        if self.last_rec is not None:
            try:
                shutil.rmtree(self.last_rec)
            except:
                pass
            self.last_rec = None

    def erase_all(self):
        try:
            shutil.rmtree(self.path)
        except:
            pass

    def rebase(self, newpath):
        for file in listdir(self.path):
            if path.isfile(path.join(self.path, file)):
                shutil.copy(path.join(self.path, file), path.join(newpath, file))
        self.path = newpath
        self.last_rec = None
