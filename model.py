import json
from os import path, remove, listdir, mkdir
import time
import copy
import shutil

class Model():

    def __init__(self, dirpath, name, new:bool):
        self.info = {}
        self.gestures = {}
        self.root = dirpath
        self.path = path.join(dirpath, name)
        self.model_path = path.join(self.path, 'model.ckpt')
        self.name = name
        self.active_gesture = None
        if new or not path.exists(self.path):
            self.create()
        else:
            self.load()

    def load(self):
        try:
            with open(path.join(self.path, 'info.json'), 'r') as f:
                self.info = json.load(f)
        except:
            self.info = Model.default_info()
        for gesture in listdir(self.path):
            if path.isdir(path.join(self.path, gesture)):
                self.gestures[gesture] = Gesture(path.join(self.path, gesture), new=False)

    def create(self):
        self.info = Model.default_info()
        try:
            mkdir(self.path)
        except:
            pass

    def add_gesture(self, name):
        if not path.exists(path.join(self.path, name)):
            self.gestures[name] = Gesture(path.join(self.path, name), new=True)

    def remove_gesture(self, name):
        try:
            self.gestures[name].erase_all()
            self.gestures.pop(name)
        except:
            pass

    def select_gesture(self, name):
        if name in self.gestures.keys():
            self.active_gesture = name

    def get_gestures(self):
        return [(name, str(gesture.recs), f'{gesture.space/1000}kB') for name, gesture in self.gestures.items()]
    
    def gesture_space(self):
        return f'{sum([gesture.space for name, gesture in self.gestures.items()])/1000}kB'
    
    @classmethod
    def default_info(_cls):
        return {}

    def save(self):
        with open(path.join(self.path, 'info.json'), 'w') as f:
            json.dump(f)

    def save_as(self, name):
        self.path = path.join(self.root, name)
        mkdir(self.path)
        for gesture in self.gestures:
            gesture = copy.deepcopy(gesture)
            gesture.rebase(path.join(self.path, gesture))
        self.save()

    def has_trained_model(self):
        return path.exists(self.model_path)

    def get_info(self):
        return [('Name', self.name),
                ('Gestures', len(self.gestures.keys())),
                ('Space', self.gesture_space()),
                ('Is trained', str(self.has_trained_model()))]

class Gesture():

    def __init__(self, dirpath, new:bool):
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