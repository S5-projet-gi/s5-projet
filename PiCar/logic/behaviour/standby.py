from typing import TYPE_CHECKING

from logic.behaviour.models import Movement, Sensors

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM


class StandbyState:
    """
    State that does nothing.
    """

    def reset(self) -> None:
        pass

    def tick(
        self,
        delta: float,
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        return Movement(0, None)
