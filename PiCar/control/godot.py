import asyncio
import json
import math

from websockets.asyncio.server import ServerConnection

from control import Control


class GoDotControl(Control):
    client: ServerConnection

    sensors: dict = {}

    def __init__(self, client: ServerConnection):
        self.client = client

    def move(self, speed):
        """Set the wheel speeds"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(
                json.dumps({"type": "control", "command": "speed", "value": speed})
            )
        )

    def stop(self):
        """Stop both wheels"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(
                json.dumps({"type": "control", "command": "speed", "value": 0})
            )
        )

    def turn_straight(self):
        """Turn the front wheels back straight"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(
                json.dumps({"type": "control", "command": "turn", "value": 0})
            )
        )

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(
                json.dumps({"type": "control", "command": "turn", "value": angle})
            )
        )

    def distance(self) -> float:
        """Measure the distance to the nearest object"""
        return self.sensors.get("distance", math.inf)

    def line(self) -> list[int]:
        """Measure the luminance of the ground"""
        return self.sensors.get("line", [0, 0, 0, 0, 0])
