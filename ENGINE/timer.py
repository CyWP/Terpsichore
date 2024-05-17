import time
from enum import Enum

class Actions(Enum):
    POP = 'pop'
    RESET = 'reset'
    RESET_ALL = 'reset_all'
    CLEAR = 'clear'
class Timer:
    """A class to manage multiple timers."""
    
    starts = []
    durations = []
    empty_indices = []
    used_indices = []
    actions = []
    num_timers = 0

    @classmethod
    def add_timer(cls, duration: float, action=Actions.POP) -> int:
        """Add a timer with the specified duration and return its index."""
        if duration < 0:
            raise ValueError(f'Negative timer duration: {duration}')
        if action not in Actions:
            raise ValueError(f'Invalid action: {action}')
        cls.num_timers += 1
        index = cls.get_index()
        cls.used_indices.append(index)
        cls.starts.insert(index, time.time())
        cls.durations.insert(index, duration)
        if action == Actions.POP:
            cls.actions.insert(index, lambda i=index: cls.pop(i))
        elif action == Actions.RESET:
            cls.actions.insert(index, lambda i=index: cls.reset(i))
        elif action == Actions.RESET_ALL:
            cls.actions.insert(index, cls.reset_all)
        elif action == Actions.CLEAR:
            cls.actions.insert(index, cls.clear)
        return index
    
    @classmethod
    def is_done(cls, index: int) -> bool:
        """Check if the timer with the given index is done."""
        is_done = time.time() - cls.starts[index] > cls.durations[index]
        if not is_done:
            return False
        cls.actions[index]()
        return True
    
    @classmethod
    def get_index(cls) -> int:
        """Get the index for a new timer."""
        if len(cls.empty_indices):
            return cls.empty_indices.pop()
        return len(cls.starts)
    
    @classmethod
    def any_timer_done(cls, reset=False, pop=False) -> bool:
        """Check if any timer is done."""
        for i in cls.used_indices:
            if time.time() - cls.starts[i] > cls.durations[i]:
                if reset:
                    cls.reset_all()
                elif pop:
                    cls.clear()
                return True
        return False
    
    @classmethod
    def all_timers_done(cls, clear=False, reset=False) -> bool:
        """Check if all timers are done."""
        for i in cls.used_indices:
            if time.time() - cls.starts[i] > cls.durations[i]:
                if reset:
                    cls.reset_all()
                elif clear:
                    cls.clear()
                return True
        return False
    
    @classmethod
    def pop(cls, index: int):
        cls.empty_indices.append(index)
        cls.used_indices.remove(index)
        cls.num_timers -= 1

    @classmethod
    def reset(cls, index: int):
        cls.starts[index] = time.time()

    @classmethod
    def reset_all(cls):
        """Reset all timer starts."""
        for i in cls.used_indices:
            cls.starts[i] = time.time()

    @classmethod
    def clear(cls):
        """Clear all timers."""
        cls.empty_indices = []
        cls.used_indices = []
        cls.num_timers = 0