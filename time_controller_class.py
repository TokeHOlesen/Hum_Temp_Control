from time import perf_counter
import constants


class TimeController:
    def __init__(self, user_input):
        self.user_input = user_input
        self.log_written = False
        self.reset()
    
    def start_timer(self):
        self.start = perf_counter()
        
    def get_remaining(self):
        return self.user_input.running_time * 60 - self.get_elapsed()
    
    def get_elapsed(self):
        return int(perf_counter() - self.start)
    
    def stop_condition(self):
        if self.user_input.running_time is not None:
            if self.user_input.running_time > 0 and self.get_remaining() <= 0:
                return True
            return False
        return False
    
    def log_condition(self):
        if self.get_elapsed() % constants.LOGGING_FREQUENCY == 0 and not self.log_written:
            self.log_written = True
            return True
        self.log_written = False
        return False
    
    def reset(self):
        self.start = None
        self.elapsed = None
        self.remaining = None