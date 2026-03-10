import math

from websockets.asyncio.server import ServerConnection

from control import Control


class GoDotControl(Control):
    client: ServerConnection

    sensors: dict = {}
    last_speed: float = 0.0
    last_steer_dir: float = 0.0

    def __init__(self, client: ServerConnection):
        self.client = client

    def move(self, speed):
        """Store speed to send to GoDot"""
        self.last_speed = speed

    def stop(self):
        """Stop both wheels"""
        self.last_speed = 0.0

    def turn_straight(self):
        """Turn the front wheels back straight"""
        self.last_steer_dir = 0.0

    def turn(self, angle):
        """Store angle to send to GoDot"""
        self.last_steer_dir = angle

    def distance(self) -> float:
        """Measure the distance to the nearest object"""
        return self.sensors.get("distance", math.inf)

    def line(self) -> list[int]:
        """Measure the luminance of the ground"""
        return self.sensors.get("line_follower", [0, 0, 0, 0, 0])
