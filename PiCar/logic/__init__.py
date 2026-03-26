import asyncio
import time

from control import Control
from logic.behaviour.fsm import BehaviourFSM, Sensors


class Logic:
    control: Control
    fsm: BehaviourFSM

    def __init__(self, control: Control):
        self.control = control
        self.fsm = BehaviourFSM()

    def __del__(self):
        self.control.stop()

    def move_toward(self, current: float, target: float, max_delta: float) -> float:
        if target > current + max_delta:
            return current + max_delta
        if target < current - max_delta:
            return current - max_delta
        return target

    async def run(self):
        # Wait for sensors to be initialized
        await asyncio.sleep(2)

        current_speed_cmd = 0.0
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

                target_speed = result.speed

                accel_rate = 20.0
                decel_rate = 50.0 # on peut decel plus vite parce que ya le capteur de ligne qui block la bille

                rate = accel_rate if target_speed > current_speed_cmd else decel_rate
                val = (rate * delta)
                current_speed_cmd = self.move_toward(current_speed_cmd, target_speed, val)

                self.control.move(current_speed_cmd)

                if result.angle is not None:
                    self.control.turn(result.angle)

                await asyncio.sleep(0.01)
            except Exception as e:
                print("Error in logic", e)
