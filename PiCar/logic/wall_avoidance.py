from dataclasses import dataclass
from enum import Enum

import logic.const as const


class AvoidanceState(Enum):
    ROTATE_LEFT = "rotate_left"
    FORWARD = "forward"
    ROTATE_RIGHT = "rotate_right"
    DONE = "done"


@dataclass
class WallAvoidanceLogic:
    """State for the wall avoidance controller."""

    active: bool = False
    state: AvoidanceState = AvoidanceState.ROTATE_LEFT
    distance_traveled: float = 0.0


class WallAvoidanceController:
    """
    Distance-based wall avoidance sequence.
    
    1. Rotate left by rotation_angle
    2. Move forward by forward_distance
    3. Rotate right by rotation_angle
    """

    def __init__(self):
        self.state = WallAvoidanceLogic()

    def trigger(self):
        self.state.active = True
        self.state.state = AvoidanceState.ROTATE_LEFT
        self.state.distance_traveled = 0.0

    def update(self, delta: float, current_steer: float = 0.0, current_speed: float = 0.0) -> tuple[float, float, bool]:
        """
        Returns (speed, steer_dir, done)
        """
        if not self.state.active:
            return 0.0, 0.0, True

        steer_dir = 0.0
        speed = 0.0
        done = False

        if self.state.state == AvoidanceState.ROTATE_LEFT:
            # Turn left
            steer_dir = const.wall_avoid_rotation_angle
            speed = const.wall_avoid_turn_speed
            # Simulate rotation complete after a moment (simplified)
            self.state.distance_traveled += delta
            if self.state.distance_traveled > 0.7:  # 0.5s to rotate
                self.state.state = AvoidanceState.FORWARD
                self.state.distance_traveled = 0.0

        elif self.state.state == AvoidanceState.FORWARD:
            # Move forward
            steer_dir = 0.0
            speed = const.wall_avoid_forward_speed
            self.state.distance_traveled += speed * delta
            if self.state.distance_traveled >= const.wall_avoid_forward_distance:
                self.state.state = AvoidanceState.ROTATE_RIGHT
                self.state.distance_traveled = 0.0

        elif self.state.state == AvoidanceState.ROTATE_RIGHT:
            # Turn right (back to original direction)
            steer_dir = -const.wall_avoid_rotation_angle
            speed = const.wall_avoid_turn_speed
            self.state.distance_traveled += delta
            if self.state.distance_traveled > 1.3:  # 0.5s to rotate
                self.state.active = False
                self.state.state = AvoidanceState.DONE
                self.state.distance_traveled = 0.0
                done = True

        return speed, steer_dir, done
