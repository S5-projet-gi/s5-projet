import asyncio
import json

from websockets.asyncio.server import ServerConnection

from control import Control


class GoDotControl(Control):
    client: ServerConnection

    def __init__(self, client: ServerConnection):
        self.client = client

    def forward(self):
        """Move both wheels forward"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "speed", "value": 10}))
        )

    def backward(self):
        """Move both wheels backward"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "speed", "value": -10}))
        )

    def stop(self):
        """Stop both wheels"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "speed", "value": 0}))
        )

    def speed(self, speed):
        """Set moving speeds"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "speed", "value": speed}))
        )

    def turn_left(self):
        """Turn the front wheels left"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "turn", "value": 180}))
        )

    def turn_straight(self):
        """Turn the front wheels back straight"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "turn", "value": 0}))
        )

    def turn_right(self):
        """Turn the front wheels right"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "turn", "value": 90}))
        )

    def turn(self, angle):
        """Turn the front wheels to the giving angle"""
        if self.client is None:
            return
        asyncio.create_task(
            self.client.send(json.dumps({"command": "turn", "value": angle}))
        )
