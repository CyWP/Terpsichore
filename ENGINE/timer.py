import time

class Timer:
    """A class to manage multiple timers."""
    
    starts = []
    durations = []
    empty_indices = []
    used_indices = []
    num_timers = 0

    @classmethod
    def add_timer(cls, duration: int) -> int:
        """Add a timer with the specified duration and return its index."""
        cls.num_timers += 1
        index = cls.get_index()
        cls.used_indices.append(index)
        cls.starts.append(time.time())
        cls.durations.append(duration)
        return index
    
    @classmethod
    def is_done(cls, index: int, reset=False, clear=False, pop=False) -> bool:
        """Check if the timer with the given index is done."""
        is_done = time.time() - cls.starts[index] > cls.durations[index]
        if not is_done:
            return False
        if reset:
            cls.starts[index] = time.time()
        elif clear:
            cls.clear()
        elif pop:
            cls.empty_indices.append(index)
            cls.used_indices.remove(index)
            cls.num_timers -= 1
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
    def reset_all(cls):
        """Reset all timer starts."""
        for i in cls.used_indices:
            cls.starts[i] = time.time()

    @classmethod
    def clear(cls):
        """Clear all timers."""
        cls.starts = []
        cls.durations = []
        cls.empty_indices = []
        cls.used_indices = []
        cls.num_timers = 0
