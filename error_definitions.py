class ValueOutsideRangeError(Exception):
    def __init__(self, message="Value is outside the allowed range."):
        super().__init__(message)
        

class MinuteValueOutsideRangeError(Exception):
    def __init__(self, message="Minute value is outside the allowed range."):
        super().__init__(message)


class ValueMissingError(Exception):
    def __init__(self, message="No value was provided."):
        super().__init__(message)