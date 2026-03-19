from __future__ import annotations

from control import Control

from . import BehaviourFSM


class StandbyState:
    """
    State that does nothing.
    """

    def reset(self) -> None:
        pass

    def tick(
        self,
        delta: float,
        control: Control,
        fsm: BehaviourFSM,
    ) -> None:
        control.move(0)
        pass
