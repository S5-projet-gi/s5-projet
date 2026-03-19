from __future__ import annotations

from typing import Protocol

from line_follow import LineFollowState
from sharp_turn import SharpTurnState
from standby import StandbyState
from wall_avoidance import WallAvoidanceState

from control import Control


class BehaviourFSM:
    """
    High-level behaviour finite-state machine.

    States:
    - LineFollowState
    - WallAvoidanceState
    - SharpTurnState (placeholder)
    """

    def __init__(self) -> None:
        self.line_follow = LineFollowState()
        self.wall_avoidance = WallAvoidanceState()
        self.sharp_turn = SharpTurnState()
        self.standby = StandbyState()

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

    def to_sharp_turn(self) -> bool:
        return self.transition_to(self.sharp_turn)

    def to_standby(self) -> bool:
        return self.transition_to(self.standby)

    def tick(
        self,
        delta: float,
        control: Control,
    ) -> None:
        return self.state.tick(delta=delta, control=control, fsm=self)


class BehaviourState(Protocol):
    def reset(self) -> None:
        raise NotImplementedError("This method must be implemented by a subclass")

    def tick(
        self,
        delta: float,
        control: Control,
        fsm: BehaviourFSM,
    ) -> None:
        raise NotImplementedError("This method must be implemented by a subclass")
