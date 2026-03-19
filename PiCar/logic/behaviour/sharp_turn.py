from __future__ import annotations

from control import Control

from . import BehaviourFSM


class SharpTurnState:
    """
    Placeholder state for future sharp-turn behaviour.

    Current behaviour:
    - Returns zero speed and zero steering for one tick.
    - Immediately transitions back to line-follow.
    """

    def reset(self) -> None:
        pass

    def tick(
        self,
        delta: float,
        control: Control,
        fsm: BehaviourFSM,
    ) -> None:
        # TODO: Implement actual sharp-turn manoeuvre.
        fsm.to_line_follow()
