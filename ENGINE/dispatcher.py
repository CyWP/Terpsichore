from abc import ABC, abstractmethod

class Dispatcher(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def dispatch(self):
        pass

    @abstractmethod
    def close(self):
        pass

class CSVWriter(Dispatcher):

    def __init__(self, filename:str):
        pass

    def dispatch(self):
        pass

    def close(self):
        pass

class OSCClient(Dispatcher):

    def __init__(self, osc):
        pass

    def dispatch(self):
        pass

    def close(self):
        pass