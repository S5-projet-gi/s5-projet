import asyncio
import time

import const
from control import Control
from logic.behaviour import BehaviourFSM


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

                distance = self.control.distance()

                # Trigger wall avoidance when distance <= 3
                if distance > 0 and distance <= const.wall_avoid_detection_distance:
                    if self.fsm.to_wall_avoidance():
                        print(f"[Logic] Wall avoidance triggered! distance={distance}")

                self.fsm.tick(
                    delta=delta,
                    control=self.control,
                )

                await asyncio.sleep(0.01)
            except Exception as e:
                print("Error in logic", e)
