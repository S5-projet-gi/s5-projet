import asyncio

from control import Control


class Logic:
    control: Control

    def __init__(self, control: Control):
        self.control = control

    async def run(self):
        while True:
            self.control.forward()
            await asyncio.sleep(1)
            self.control.stop()
            await asyncio.sleep(1)
