from datetime import datetime
from time import time
import constants


class TimeController:
    def __init__(self, user_input) -> None:
        self.user_input = user_input
        self.log_written = False
        self.temp_reached_timestamp = None
        self.timer_restarted = False
        self.delayed_startup_time = 0
        self.reset()
    
    def set_delayed_startup_time(self, delay) -> None:
        self.delayed_startup_time = time() + delay * 60 # Change to 3600 when done testing
        
    def clear_delayed_startup_time(self) -> None:
        self.delayed_startup_time = 0
    
    def start_timer(self) -> None:
        self.start = time()
        
    def restart_timer(self) -> None:
        if not self.timer_restarted:
            self.start = time()
            self.timer_restarted = True
    
    def set_temp_reached_timestamp(self) -> None:
        if self.temp_reached_timestamp is None:
            self.temp_reached_timestamp = time()
            
    def start_dht22_quarantine(self) -> None:
        self.quarantine_start = time()
    
    @property
    def delayed_startup_time_reached(self) -> bool:
        if time() >= self.delayed_startup_time:
            return True
        return False

    @property
    def delayed_startup_text(self) -> str:
        return datetime.fromtimestamp(self.delayed_startup_time).strftime("%d-%m-%Y %H:%M")
            
    @property
    def seconds_remaining(self) -> int:
        return self.user_input.running_time * 60 - self.seconds_elapsed
    
    @property
    def seconds_elapsed(self) -> int:
        return int(time() - self.start)
    
    @property
    def seconds_elapsed_since_temp_reached(self) -> int:
        return int(time() - self.temp_reached_timestamp)
    
    @property
    def elapsed_h_m_s(self) -> tuple[int, int, int]:
        elapsed_hours, remainder  = divmod(self.seconds_elapsed, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        return elapsed_hours, elapsed_minutes, elapsed_seconds
    
    @property
    def remaining_h_m_s(self) -> tuple[int, int, int]:
        remaining_hours, remainder  = divmod(self.seconds_remaining, 3600)
        remaining_minutes, remaining_seconds = divmod(remainder, 60)
        return remaining_hours, remaining_minutes, remaining_seconds
    
    @property
    def stop_condition(self) -> bool:
        if self.user_input.running_time is not None:
            if self.user_input.running_time > 0 and self.seconds_remaining <= 0:
                return True
            return False
        return False
    
    @property
    def log_condition(self) -> bool:
        if self.seconds_elapsed % constants.LOGGING_FREQUENCY == 0 and not self.log_written:
            self.log_written = True
            return True
        self.log_written = False
        return False
    
    @property
    def seconds_in_quarantine(self) -> int:
        """Returns how much time has elapsed since the DHT22 quarantine started (in seconds)"""
        return int(time() - self.quarantine_start)
    
    def reset(self) -> None:
        self.temp_reached_timestamp = None
        self.start = None
        self.elapsed = None
        self.remaining = None
        self.timer_restarted = False
        self.clear_delayed_startup_time()
        