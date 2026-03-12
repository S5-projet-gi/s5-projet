import asyncio
import math
import time

import RPi.GPIO as GPIO


class PiCarUltrasonic:
    TRIG_PIN = 12
    ECHO_PIN = 16

    distance = math.inf
    ratio = 0.3

    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)
        GPIO.output(self.TRIG_PIN, False)

        asyncio.create_task(self.measure_distance_task())

    async def measure_distance_task(self):
        await asyncio.sleep(2)
        self.distance = 0

        while True:
            GPIO.output(self.TRIG_PIN, True)
            time.sleep(0.00001)
            GPIO.output(self.TRIG_PIN, False)

            pulse_start = time.time()
            pulse_end = time.time()

            while GPIO.input(self.ECHO_PIN) == 0:
                pulse_start = time.time()
            while GPIO.input(self.ECHO_PIN) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            mesure = 1.0546 * round(pulse_duration * 16666, 2) - 4.0464
            self.distance = self.ratio * mesure + (1 - self.ratio) * self.distance
            await asyncio.sleep(0.03)
