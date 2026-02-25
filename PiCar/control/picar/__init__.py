from control import Control


class PiCarControl(Control):
    from control.picar.ultrasonic import PiCarUltrasonic
    from SunFounder.back_wheels import Back_Wheels
    from SunFounder.front_wheels import Front_Wheels

    back_wheels: Back_Wheels
    front_wheels: Front_Wheels
    ultrasonic: PiCarUltrasonic

    def __init__(self):
        self.back_wheels = self.Back_Wheels(debug=True)
        self.front_wheels = self.Front_Wheels(debug=True)
        self.ultrasonic = self.PiCarUltrasonic()

    def move(self, speed):
        """Set the wheel speeds"""
        if speed >= 0:
            self.back_wheels.forward()
        else:
            self.back_wheels.backward()

        self.back_wheels.speed = abs(speed)

    def stop(self):
        """Stop both wheels"""
        self.back_wheels.stop()

    def turn_straight(self):
        """Turn the front wheels back straight"""
        self.front_wheels.turn_straight()

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        self.front_wheels.turn(angle + self.front_wheels._straight_angle)

    def distance(self) -> float:
        """Measure the distance to the nearest object"""
        return self.ultrasonic.distance
