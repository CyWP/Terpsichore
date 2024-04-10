from appstate import AppState
import csv
from pythonosc.udp_client import SimpleUDPClient
from .tasks import Tasks

class Dispatcher:
    """
    Base class for dispatchers.
    """

    def dispatch(self, mvmt, pose, gesture, exts):
        pass

    def start(self):
        pass

    def close(self):
        pass

class CSVWriter(Dispatcher):
    """
    Dispatcher for writing data to a CSV file.
    """

    def __init__(self):
        self.data = []
        self.outfile = AppState.get_csv_file()

    def dispatch(self, mvmt, pose, gesture, exts):
        self.data.append(mvmt)

    def close(self, err=False):
        """
        Closes the CSVWriter by writing the internal data to a CSV file if not closed due to an error.

        Args:
            err: Defines if function was called because of error.
        """
        if not err:
            with open(self.outfile, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(self.data)

class OSCClient(Dispatcher):
    """
    Dispatcher for sending data over OSC (Open Sound Control) protocol.
    """

    def __init__(self):

        ip = AppState.get_attr('osc_ip')
        port = AppState.get_attr('osc_port')
        self.address = AppState.get_attr('osc_address')
        self.client = SimpleUDPClient(ip, port)

    def start(self):
        self.client.send_message(address=f'{self.address}/start', value=True)

    def dispatch(self, mvmt, pose, gesture, exts):

        self.client.send_message(address=f'{self.address}/mvmt', value=mvmt.tolist())
        self.client.send_message(address=f'{self.address}/pose', value=pose.tolist())
        self.client.send_message(address=f'{self.address}/class', value=gesture.tolist())
        self.client.send_message(address=f'{self.address}/exts', value=exts.tolist())

    def close(self, err=False):
        """
        Closes the OSCClient dispatcher by sending a completion message.
        """
        self.client.send_message(address=f'{self.address}/done', value=True)

def get_dispatcher(task: str):
    """
    Factory function to get the appropriate dispatcher based on the task.
    
    Args:
        task (str): Task type, either 'perform' or 'record'.
    
    Returns:
        Dispatcher: An instance of the appropriate dispatcher.
    
    Raises:
        ValueError: If the task type is invalid.
    """
    if task == Tasks.PERFORM:
        return OSCClient()
    elif task == Tasks.RECORD:
        return CSVWriter()
    else:
        raise ValueError(f'Invalid task type: {task}')