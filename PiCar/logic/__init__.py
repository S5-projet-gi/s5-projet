import asyncio
import time

from control import Control
from logic.behaviour import BehaviourFSM, Sensors


class Logic:
    control: Control
    fsm: BehaviourFSM

    def __init__(self, control: Control):
        self.control = control
        self.fsm = BehaviourFSM()

    def __del__(self):
        self.control.stop()

    async def run(self):
        # Wait for sensors to be initialized
        await asyncio.sleep(2)

        last_time = time.monotonic()

        while True:
            try:
                now = time.monotonic()
                delta = now - last_time
                last_time = now

                sensors = Sensors(self.control.line(), self.control.distance())
                result = self.fsm.tick(delta, sensors)
                while result is None:
                    result = self.fsm.tick(delta, sensors)

                # TODO: Make progressive acceleration
                self.control.move(result.speed)
                if result.angle is not None:
                    self.control.turn(result.angle)

                await asyncio.sleep(0.01)
            except Exception as e:
                print("Error in logic", e)
