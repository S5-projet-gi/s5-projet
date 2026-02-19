class Control:
    def __init__(self):
        raise NotImplementedError("This method must be implemented by a subclass")

    def forward(self):
        """Move both wheels forward"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def backward(self):
        """Move both wheels backward"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def stop(self):
        """Stop both wheels"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def speed(self, speed):
        """Set moving speeds"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn_left(self):
        """Turn the front wheels left"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn_straight(self):
        """Turn the front wheels back straight"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn_right(self):
        """Turn the front wheels right"""
        raise NotImplementedError("This method must be implemented by a subclass")

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        raise NotImplementedError("This method must be implemented by a subclass")
