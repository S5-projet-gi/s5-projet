import asyncio

from control import Control


class Logic:
    control: Control

    def __init__(self, control: Control):
        self.control = control

    def __del__(self):
        self.control.stop()

    async def run(self):
        # Wait for sensors to be initialized
        await asyncio.sleep(2)

        while True:
            try:
                self.control.move(30)
                await asyncio.sleep(1)
                self.control.stop()
                await asyncio.sleep(1)
                self.control.move(-30)
                await asyncio.sleep(1)
            except Exception as e:
                print("Error in logic", e)
