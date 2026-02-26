from control import Control


class PiCarControl(Control):
    from control.picar.line import PiCarLine
    from control.picar.ultrasonic import PiCarUltrasonic
    from SunFounder.back_wheels import Back_Wheels
    from SunFounder.front_wheels import Front_Wheels
    from SunFounder.SunFounder_PCA9685 import PCA9685

    _line: PiCarLine
    _ultrasonic: PiCarUltrasonic
    _back_wheels: Back_Wheels
    _front_wheels: Front_Wheels

    def __init__(self):
        pwm = self.PCA9685.PWM(bus_number=1)
        pwm.setup()
        pwm.frequency = 60

        self._line = self.PiCarLine()
        self._ultrasonic = self.PiCarUltrasonic()
        self._back_wheels = self.Back_Wheels(debug=True)
        self._front_wheels = self.Front_Wheels(debug=True)

    def move(self, speed):
        """Set the wheel speeds"""
        if speed >= 0:
            self._back_wheels.forward()
        else:
            self._back_wheels.backward()

        self._back_wheels.speed = abs(speed)

    def stop(self):
        """Stop both wheels"""
        self._back_wheels.stop()

    def turn_straight(self):
        """Turn the front wheels back straight"""
        self._front_wheels.turn_straight()

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        self._front_wheels.turn(angle + self._front_wheels._straight_angle)

    def distance(self) -> float:
        """Measure the distance to the nearest object"""
        return self._ultrasonic.distance

    def line(self) -> list[int]:
        """Measure the luminance of the ground"""
        return self._line.line
        raise NotImplementedError("This method must be implemented by a subclass")
