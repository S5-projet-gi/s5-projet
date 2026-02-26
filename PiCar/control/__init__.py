class Control:
    def __init__(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def move(self, speed):
        """Set the wheel speeds"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def stop(self):
        """Stop both wheels"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn_straight(self):
        """Turn the front wheels back straight"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def distance(self) -> float:
        """Measure the distance to the nearest object"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def line(self) -> list[int]:
        """Measure the luminance of the ground"""
        raise NotImplementedError("This method must be implemented by a subclass")
