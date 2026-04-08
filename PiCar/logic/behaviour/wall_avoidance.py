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
    FOURTH = "fourth"


class WallAvoidanceState:
    """
    Dedicated wall-avoidance FSM state with integrated controller logic.

    Sequence:
    1) Rotate right backwards (point car left)
    2) Move forward (skip wall)
    3) Rotate right (reach line)
    3) Rotate left (align to line)
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
        if self.phase == AvoidancePhase and sensors.speed > 0:
            return Movement(
                0,
                0,
            )

        self.distance_parcourue += delta * const.picar["distance_rate"]

        match self.phase:
            case AvoidancePhase.FIRST:
                if self.distance_parcourue >= const.wall_avoidance["first_time"]:
                    self.phase = AvoidancePhase.SECOND
                    self.distance_parcourue = 0.0
                    print(f"[WallAvoidance] Phase 1 complete, switching to phase 2")
                    return
                print(
                    f"[WallAvoidance] Phase 1 - distance_parcourue={self.distance_parcourue}"
                )
                return Movement(
                    const.wall_avoidance["first_speed"],
                    const.wall_avoidance["first_angle"],
                )
            case AvoidancePhase.SECOND:
                if self.distance_parcourue >= const.wall_avoidance["second_time"]:
                    self.phase = AvoidancePhase.THIRD
                    self.distance_parcourue = 0.0
                    print(f"[WallAvoidance] Phase 2 complete, switching to phase 3")
                    return
                print(
                    f"[WallAvoidance] Phase 2 - distance_parcourue={self.distance_parcourue}"
                )
                return Movement(
                    const.wall_avoidance["second_speed"],
                    const.wall_avoidance["second_angle"],
                )
            case AvoidancePhase.THIRD:
                if any([x != 0 for x in sensors.line]):
                    self.phase = AvoidancePhase.FOURTH
                    self.distance_parcourue = 0.0
                    print(f"[WallAvoidance] Phase 3 complete, switching to phase 4")
                    return
                print(
                    f"[WallAvoidance] Phase 3 - distance_parcourue={self.distance_parcourue}"
                )
                return Movement(
                    const.wall_avoidance["third_speed"],
                    const.wall_avoidance["third_angle"],
                )
            case AvoidancePhase.FOURTH:
                if sensors.line == [0, 0, 2, 0, 0]:
                    fsm.to_line_follow()
                    print(f"[WallAvoidance] Phase 4 complete, switching to line follow")
                    return
                print(
                    f"[WallAvoidance] Phase 4 - distance_parcourue={self.distance_parcourue}"
                )
                return Movement(
                    const.wall_avoidance["fourth_speed"],
                    const.wall_avoidance["fourth_angle"],
                )
