from . import BehaviourFSM, Movement, Sensors


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
        fsm: BehaviourFSM,
    ) -> Movement | None:
        return Movement(0, None)
