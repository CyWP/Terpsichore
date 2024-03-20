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
        if new or not path.exists(self.path):
            self.create()
        else:
            self.load()

    def load(self):
        with open(path.join(self.path, 'info.json'), 'r') as f:
            self.info = json.load(f)
        for gesture in listdir(self.path):
            if path.isfile(path.join(self.path, gesture)):
                self.gestures[gesture] = Gesture(gesture, new=False)

    def create(self):
        self.info = Model.default_info()
        mkdir(self.path)

    def add_gesture(self, name):
        if not path.exists(path.join(self.path, name)):
            self.gestures[name] = Gesture(name)

    def remove_gesture(self, name):
        try:
            self.gestures.pop(name)
        except:
            pass
    
    @classmethod
    def default_info(_cls):
        return {}

    def save(self):
        with open(path.join(self.path, 'info.json'), 'w') as f:
            json.dump(f)

    def save_as(self, name):
        self.path = path.join(self.root, name)
        for gesture in self.gestures:
            gesture = copy.deepcopy(gesture)
            gesture.rebase(path.join(self.path, gesture))
        self.save()

class Gesture():

    def __init__(self, dirpath, new:bool):
        self.path = dirpath
        self.last_rec = None
        if new or path.exists(self.path):
            self.create()
        else:
            self.load()

    def create(self):
        self.space = 0
        self.recs = 0            

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
                remove(self.last_rec)
            except:
                pass
            self.last_rec = None

    def rebase(self, newpath):
        for file in listdir(self.path):
            if path.isfile(path.join(self.path, file)):
                shutil.copy(path.join(self.path, file), path.join(newpath, file))
        self.path = newpath
        self.last_rec = None