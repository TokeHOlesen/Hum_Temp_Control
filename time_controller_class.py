from time import perf_counter
import constants


class TimeController:
    def __init__(self, user_input):
        self.user_input = user_input
        self.log_written = False
        self.reset()
    
    def start_timer(self):
        self.start = perf_counter()
    
    @property
    def seconds_remaining(self):
        return self.user_input.running_time * 60 - self.seconds_elapsed
    
    @property
    def seconds_elapsed(self):
        return int(perf_counter() - self.start)
    
    @property
    def elapsed_h_m_s(self):
        elapsed_hours, remainder  = divmod(self.seconds_elapsed, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        return elapsed_hours, elapsed_minutes, elapsed_seconds
    
    @property
    def remaining_h_m_s(self):
        remaining_hours, remainder  = divmod(self.seconds_remaining, 3600)
        remaining_minutes, remaining_seconds = divmod(remainder, 60)
        return remaining_hours, remaining_minutes, remaining_seconds
    
    @property
    def stop_condition(self):
        if self.user_input.running_time is not None:
            if self.user_input.running_time > 0 and self.seconds_remaining <= 0:
                return True
            return False
        return False
    
    @property
    def log_condition(self):
        if self.seconds_elapsed % constants.LOGGING_FREQUENCY == 0 and not self.log_written:
            self.log_written = True
            return True
        self.log_written = False
        return False
    
    def reset(self):
        self.start = None
        self.elapsed = None
        self.remaining = None