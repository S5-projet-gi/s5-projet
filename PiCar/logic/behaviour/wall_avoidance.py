from __future__ import annotations

from enum import Enum

import const
from control import Control

from . import BehaviourFSM


class AvoidancePhase(Enum):
    ROTATE_LEFT = "rotate_left"
    FORWARD = "forward"
    ROTATE_RIGHT = "rotate_right"


class WallAvoidanceState:
    """
    Dedicated wall-avoidance FSM state with integrated controller logic.

    Sequence:
    1) Rotate left
    2) Move forward
    3) Rotate right
    4) Transition back to line follow
    """

    phase: AvoidancePhase = AvoidancePhase.ROTATE_LEFT
    distance_traveled: float = 0.0

    def reset(self) -> None:
        self.phase = AvoidancePhase.ROTATE_LEFT
        self.distance_traveled = 0.0

    def tick(
        self,
        delta: float,
        control: Control,
        fsm: BehaviourFSM,
    ) -> None:
        self.distance_traveled += delta
        if self.distance_traveled > 1.3:
            fsm.to_line_follow()
            return

        match self.phase:
            case AvoidancePhase.ROTATE_LEFT:
                control.turn(const.wall_avoid_rotation_angle)
                control.move(const.wall_avoid_turn_speed)
            case AvoidancePhase.FORWARD:
                control.turn(0)
                control.move(const.wall_avoid_forward_speed)
            case AvoidancePhase.ROTATE_RIGHT:
                control.turn(-const.wall_avoid_rotation_angle)
                control.move(const.wall_avoid_turn_speed)
