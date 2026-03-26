from enum import Enum
from typing import TYPE_CHECKING

import const
from logic.behaviour.models import Movement, Sensors

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM

class Turn90Phase(Enum):
    FIRST = "first"
    SECOND = "second"

class SharpTurnState:
    """
    Placeholder state for future sharp-turn behaviour.

    Current behaviour:
    - Returns zero speed and zero steering for one tick.
    - Immediately transitions back to line-follow.
    """

    direction = 1
    phase: Turn90Phase = Turn90Phase.FIRST
    distance_parcourue: float = 0.0

    def reset(self) -> None:
        self.phase = Turn90Phase.FIRST
        self.distance_parcourue = 0.0

    def tick(
        self,
        delta: float,
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        self.distance_parcourue += delta
        
        match self.phase:
            case Turn90Phase.FIRST:
                if self.distance_parcourue >= const.two_point_turn["first_distance"]:
                    self.distance_parcourue = 0.0
                    self.phase = Turn90Phase.SECOND
                return Movement(
                  const.two_point_turn["first_speed"],
                  const.two_point_turn["first_angle"],
                )
            case Turn90Phase.SECOND:
                if self.distance_parcourue >= const.two_point_turn["second_distance"]:
                    self.distance_parcourue = 0.0
                    fsm.to_line_follow()
                return Movement(
                    const.two_point_turn["second_speed"],
                    self.direction * const.two_point_turn["second_angle"],
                )