from enum import Enum
from typing import TYPE_CHECKING

import const
from logic.behaviour.models import Movement, Sensors

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM


class AvoidancePhase(Enum):
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"


class WallAvoidanceState:
    """
    Dedicated wall-avoidance FSM state with integrated controller logic.

    Sequence:
    1) Rotate right backwards (point car left)
    2) Move forward (skip wall)
    3) Rotate right (reach line)
    4) Transition back to line follow
    """

    phase: AvoidancePhase = AvoidancePhase.FIRST
    distance_parcourue: float = 0.0

    def reset(self) -> None:
        self.phase = AvoidancePhase.FIRST
        self.distance_parcourue = 0.0

    def tick(
        self,
        delta: float,
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        self.distance_parcourue += delta

        match self.phase:
            case AvoidancePhase.FIRST:
                if self.distance_parcourue >= const.wall_avoidance["first_time"]:
                    self.phase = AvoidancePhase.SECOND
                    self.distance_parcourue = 0.0
                    print(f"[WallAvoidance] Phase 1 complete, switching to phase 2")
                print(f"[WallAvoidance] Phase 1 - distance_parcourue={self.distance_parcourue}")
                return Movement(
                    const.wall_avoidance["first_speed"],
                    const.wall_avoidance["first_angle"],
                )
            case AvoidancePhase.SECOND:
                if self.distance_parcourue >= const.wall_avoidance["second_time"]:
                    self.phase = AvoidancePhase.THIRD
                    self.distance_parcourue = 0.0
                    print(f"[WallAvoidance] Phase 2 complete, switching to phase 3")
                print(f"[WallAvoidance] Phase 2 - distance_parcourue={self.distance_parcourue}")
                return Movement(
                    const.wall_avoidance["second_speed"],
                    const.wall_avoidance["second_angle"],
                )
            case AvoidancePhase.THIRD:
                if self.distance_parcourue >= const.wall_avoidance["third_time"]:
                    fsm.to_line_follow()
                    print(f"[WallAvoidance] Phase 3 complete, switching to line follow")
                print(f"[WallAvoidance] Phase 3 - distance_parcourue={self.distance_parcourue}")
                return Movement(
                    const.wall_avoidance["third_speed"],
                    const.wall_avoidance["third_angle"],
                )
