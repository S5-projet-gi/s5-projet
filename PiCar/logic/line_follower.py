from __future__ import annotations

from collections import deque
from typing import Deque, Iterable, Sequence

import logic.const as const


class LineFollowerLogic:
    def __init__(self) -> None:
        self.steer_dir: float = 0.0
        self.speed: float = const.low_speed
        self._dir_buf: Deque[float] = deque(maxlen=const.dir_buffer_size)

    def reset(self) -> None:
        self.steer_dir = 0.0
        self.speed = const.low_speed
        self._dir_buf.clear()

    def update(
        self,
        delta: float,
        line_follower_array: Sequence[int] | Iterable[bool],
    ) -> tuple[float, float]:
        """
        Compute (speed, steer_dir) from line follower sensors.

        Sensor layout is expected to be:
            [left, mid-left, middle, mid-right, right]
        where each value is truthy if that sensor detects the line.
        """
        lf = list(line_follower_array)
        if len(lf) != 5:
            raise ValueError("line_follower_array must have 5 elements")

        temp_dir = self.steer_dir

        if lf[2]:
            # Middle
            temp_dir = 0.0
            self.speed = const.mid_speed
        elif lf[4]:
            # Right
            if temp_dir > -const.turn_angle_big:
                temp_dir += -delta * const.turn_accel
            else:
                temp_dir = -const.turn_angle_big
            self.speed = const.mid_speed
        elif lf[0]:
            # Left
            if temp_dir < const.turn_angle_big:
                temp_dir += delta * const.turn_accel
            else:
                temp_dir = const.turn_angle_big
            self.speed = const.mid_speed
        elif lf[1]:
            # Middle Left
            if temp_dir < const.turn_angle_mid:
                temp_dir += delta * const.turn_accel
            else:
                temp_dir = const.turn_angle_mid
            self.speed = const.low_speed
        elif lf[3]:
            # Middle Right
            if temp_dir > -const.turn_angle_mid:
                temp_dir += -delta * const.turn_accel
            else:
                temp_dir = -const.turn_angle_mid
            self.speed = const.low_speed
        else:
            # No sensor active: fall back to average direction buffer
            mean_dir = self._average(self._dir_buf)
            if mean_dir > const.turn_angle_mid:
                temp_dir = const.turn_angle_big
            elif 0 <= mean_dir < const.turn_angle_mid:
                temp_dir = const.turn_angle_mid
            elif mean_dir < -const.turn_angle_mid:
                temp_dir = -const.turn_angle_big
            elif -const.turn_angle_mid <= mean_dir < 0:
                temp_dir = -const.turn_angle_mid
            else:
                temp_dir = 0.0
            self.speed = const.low_speed

        # All sensors active -> stop
        if all(lf):
            self.speed = 0.0

        # Acceleration behavior (similar to car_speed in GoDot)
        if self.speed != 0.0 and self.speed < const.max_speed:
            self.speed = min(
                self.speed + (delta * const.accel_rate),
                const.max_speed,
            )

        self.steer_dir = temp_dir
        self._dir_buf.append(temp_dir)
        return self.speed, self.steer_dir

    @staticmethod
    def _average(values: Deque[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
