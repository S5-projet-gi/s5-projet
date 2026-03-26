from typing import TYPE_CHECKING

from logic.behaviour.models import Movement, Sensors

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM


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
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        # TODO: Implement actual sharp-turn manoeuvre.
        fsm.to_line_follow()
        return Movement(0.0, 0.0)
