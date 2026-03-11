from __future__ import annotations

from typing import Iterable, Sequence

import logic.const as const


class LineFollowerLogic:
    def __init__(self) -> None:
        self.steer_dir: float = 0.0
        self.speed: float = const.low_speed
        self.finished: bool = False  # Flag pour fin de course

    def reset(self) -> None:
        self.steer_dir = 0.0
        self.speed = const.low_speed
        self.finished = False  # Reset le flag aussi

    def update(
        self,
        delta: float,
        line_follower_array: Sequence[int] | Iterable[bool],
    ) -> tuple[float, float]:

        lf = list(line_follower_array)
        print(f"[LineFollower] input lf={lf}, types={[type(x).__name__ for x in lf]}")

        # Si déjà terminé, rester bloqué à 0,0
        if self.finished:
            print("[LineFollower] FINISHED - waiting for reset")
            return 0.0, 0.0

        if len(lf) != 5:
            raise ValueError("line_follower_array must have 5 elements")

        # ordre : [left, mid-left, middle, mid-right, right]
        weights = [-2, -1, 0, 1, 2]

        active = []
        for i in range(5):
            if lf[i]:
                active.append(weights[i])

        # -------------------------
        # Cas spécial : tous actifs = FIN DE COURSE
        # -------------------------
        if len(active) == 5:
            self.finished = True  # Marquer comme terminé
            self.speed = 0.0
            self.steer_dir = 0.0
            print("[LineFollower] ALL SENSORS ACTIVE - FINISHED!")
            return self.speed, self.steer_dir

        # -------------------------
        # Cas : aucun capteur
        # -------------------------
        if not active:
            steer = self.steer_dir
            self.speed = const.low_speed
            print(f"[LineFollower] active={active}")


        else:
            # position moyenne de la ligne
            position = sum(active) / len(active)
            #print(f"[LineFollower] active={active}, position={position:.2f}")
            # normalisation entre -1 et 1
            steer = position / 2

            # vitesse selon stabilité
            if abs(steer) < 0.2:
                self.speed = const.mid_speed
            else:
                self.speed = const.low_speed

        # accélération progressive
        if self.speed > 0 and self.speed < const.max_speed:
            self.speed = min(
                self.speed + delta * const.accel_rate,
                const.max_speed,
            )

        self.steer_dir = steer
        #print(f"[LineFollower] line={lf}, steer={steer:.2f}, speed={self.speed:.2f}")
        return self.speed, self.steer_dir

    @staticmethod
    def _average(values: Deque[float]) -> float:
        if not values:
            return 0.0
        return sum(values) / len(values)
