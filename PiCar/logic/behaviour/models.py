from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM


@dataclass
class Sensors:
    line: list[int]
    distance: float
    speed: float
    angle: float


@dataclass
class Movement:
    speed: float
    angle: float | None


class BehaviourState(Protocol):
    def reset(self) -> None:
        raise NotImplementedError("This method must be implemented by a subclass")

    def tick(
        self,
        delta: float,
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        raise NotImplementedError("This method must be implemented by a subclass")
