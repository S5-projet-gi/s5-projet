import asyncio
import sys
import time

import pytweening

import const
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

        target_angle = 0
        start_angle = 0
        current_angle = 0
        total_time_angle = 0
        current_time_angle = 0

        target_speed = 0.0
        start_speed = 0.0
        current_speed = 0.0
        total_time_speed = 0.0
        current_time_speed = 0.0

        last_time = time.monotonic()

        backwards_mult = -1 if "back" in sys.argv else 1

        while True:
            try:
                now = time.monotonic()
                delta = now - last_time
                last_time = now

                sensors = Sensors(
                    self.control.line(),
                    self.control.distance(),
                    current_speed,
                    current_angle,
                )
                result = self.fsm.tick(delta, sensors)
                while result is None:
                    result = self.fsm.tick(delta, sensors)

                # Handle speed easing
                if backwards_mult * result.speed != target_speed:
                    target_speed = backwards_mult * result.speed
                    start_speed = current_speed
                    total_time_speed = (
                        abs(target_speed - start_speed)
                        / const.picar["speed_accel_rate"]
                    )
                    current_time_speed = 0
                    print(
                        f"[Logic] New target speed: {target_speed:.2f} (current: {current_speed:.2f})"
                    )

                if (
                    current_speed != target_speed
                    and total_time_speed >= current_time_speed
                ):
                    ratio = pytweening.easeOutSine(
                        current_time_speed / total_time_speed
                    )
                    current_time_speed += delta
                    current_speed = int(
                        start_speed + ratio * (target_speed - start_speed)
                    )
                    self.control.move(current_speed)
                    print(
                        f"[Logic] Accelerating - target={target_speed:.2f}, current={current_speed:.2f}, ratio={ratio:.2f}"
                    )

                if (
                    result.angle is not None
                    and backwards_mult * result.angle != target_angle
                ):
                    target_angle = backwards_mult * result.angle
                    start_angle = current_angle
                    total_time_angle = (
                        abs(target_angle - start_angle)
                        / const.picar["angle_accel_rate"]
                    )
                    current_time_angle = 0
                    print(
                        f"[Logic] New target angle: {target_angle:.2f} (current: {current_angle:.2f})"
                    )

                if (
                    current_angle != target_angle
                    and total_time_angle >= current_time_angle
                ):
                    ratio = pytweening.easeOutSine(
                        current_time_angle / total_time_angle
                    )
                    current_time_angle += delta
                    angle = start_angle + ratio * (target_angle - start_angle)
                    self.control.turn(angle)
                    current_angle = angle
                    print(
                        f"[Logic] Turning - target={target_angle:.2f}, current={current_angle:.2f}, ratio={ratio:.2f}"
                    )

                await asyncio.sleep(0.01)
            except Exception as e:
                print("Error in logic", e)
