import asyncio

from control import Control


class Logic:
    control: Control

    def __init__(self, control: Control):
        self.control = control

    def __del__(self):
        self.control.stop()

    async def run(self):
        while True:
            self.control.speed(30)
            await asyncio.sleep(1)
            self.control.stop()
            await asyncio.sleep(1)
