import asyncio
import time

from control import Control
from logic.line_follower import LineFollowerLogic
from logic.wall_avoidance import WallAvoidanceController


class Logic:
    control: Control

    def __init__(self, control: Control):
        self.control = control
        self.line_follower = LineFollowerLogic()
        self.wall_avoidance = WallAvoidanceController()

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

                # Trigger wall avoidance (copied from GoDot logic thresholds)
                if (20 < distance < 30) or (distance < 0.3):
                    if not self.wall_avoidance.state.active:
                        self.wall_avoidance.trigger()

                if self.wall_avoidance.state.active:
                    speed, steer_dir, done = self.wall_avoidance.update(delta)
                    if done:
                        self.line_follower.reset()
                else:
                    sensors = getattr(self.control, "sensors", {})
                    line_follower_array = sensors.get("line_follower", [0, 0, 0, 0, 0])

                    if (
                        not isinstance(line_follower_array, (list, tuple))
                        or len(line_follower_array) != 5
                    ):
                        line_follower_array = [0, 0, 0, 0, 0]
                    else:
                        line_follower_array = [
                            1 if bool(v) else 0 for v in line_follower_array
                        ]

                    speed, steer_dir = self.line_follower.update(
                        delta=delta,
                        line_follower_array=line_follower_array,
                    )

                self.control.move(speed)
                self.control.turn(steer_dir)

                await asyncio.sleep(0.01)
            except Exception as e:
                print("Error in logic", e)
