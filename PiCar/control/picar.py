from control import Control


class PiCarControl(Control):
    from SunFounder.back_wheels import Back_Wheels
    from SunFounder.front_wheels import Front_Wheels

    back_wheels: Back_Wheels
    front_wheels: Front_Wheels

    def __init__(self):
        self.back_wheels = self.Back_Wheels(debug=True)
        self.front_wheels = self.Front_Wheels(debug=True)

    def forward(self):
        """Move both wheels forward"""
        self.back_wheels.forward()

    def backward(self):
        """Move both wheels backward"""
        self.back_wheels.backward()

    def stop(self):
        """Stop both wheels"""
        self.back_wheels.stop()

    def speed(self, speed):
        """Set moving speeds"""
        self.back_wheels.speed = speed

    def turn_left(self):
        """Turn the front wheels left"""
        self.front_wheels.turn_left()

    def turn_straight(self):
        """Turn the front wheels back straight"""
        self.front_wheels.turn_straight()

    def turn_right(self):
        """Turn the front wheels right"""
        self.front_wheels.turn_right()

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        self.front_wheels.turn(angle)
