from __future__ import annotations

from logic.behaviour.line_follow import LineFollowState
from logic.behaviour.models import BehaviourState, Movement, Sensors
from logic.behaviour.sharp_turn import SharpTurnState
from logic.behaviour.standby import StandbyState
from logic.behaviour.wall_avoidance import WallAvoidanceState


class BehaviourFSM:
    """
    High-level behaviour finite-state machine.

    States:
    - LineFollowState
    - WallAvoidanceState
    - SharpTurnState
    - StandbyState
    """

    state: BehaviourState

    def __init__(self) -> None:
        self.line_follow = LineFollowState()
        self.wall_avoidance = WallAvoidanceState()
        self.sharp_turn = SharpTurnState()
        self.standby = StandbyState()

        self.state = self.standby
        self.transition_to(self.line_follow)

    def transition_to(self, new_state: BehaviourState) -> bool:
        if self.state is new_state:
            return False
        self.state = new_state
        self.state.reset()
        return True

    def to_line_follow(self) -> bool:
        return self.transition_to(self.line_follow)

    def to_wall_avoidance(self) -> bool:
        return self.transition_to(self.wall_avoidance)

    def to_sharp_turn(self, direction: int) -> bool:
        self.sharp_turn.direction = direction
        return self.transition_to(self.sharp_turn)

    def to_standby(self) -> bool:
        return self.transition_to(self.standby)

    def tick(
        self,
        delta: float,
        sensors: Sensors,
    ) -> Movement | None:
        return self.state.tick(delta=delta, sensors=sensors, fsm=self)
