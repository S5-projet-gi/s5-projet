from __future__ import annotations

import const
from control import Control

from . import BehaviourFSM


class LineFollowState:
    """
    Dedicated line-follow behaviour state.

    This state delegates low-level steering/speed decisions to
    `LineFollowerLogic` and can request transitions through the FSM wrapper.
    """

    last_turn_direction = 0

    def reset(self) -> None:
        self.last_turn_direction = 0

    def tick(
        self,
        delta: float,
        control: Control,
        fsm: BehaviourFSM,
    ) -> None:
        lf = list(control.line())
        print(f"[LineFollower] input lf={lf}, types={[type(x).__name__ for x in lf]}")

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
            print("[LineFollower] ALL SENSORS ACTIVE - FINISHED!")
            fsm.to_standby()
            return

        # -------------------------
        # Cas : aucun capteur
        # -------------------------
        if not active:
            if self.last_turn_direction != 0:
                print(
                    f"[LineFollower] LOST - last turn direction={self.last_turn_direction}"
                )
                control.turn(self.last_turn_direction * const.picar["max_turn_angle"])
                control.move(const.low_speed)
                fsm.to_sharp_turn()
                return

            control.move(const.low_speed)
            print("[LineFollower] LOST - moving forward")
            return

        # position moyenne de la ligne
        position = sum(active) / len(active)
        # print(f"[LineFollower] active={active}, position={position:.2f}")
        # normalisation entre -1 et 1
        if position == -2 or position == 2:
            steer = position / 2 * const.line_follower_max_turn_angle
        else:
            steer = position / 2 * const.line_follower_med_turn_angle

        if position != 0:
            self.last_turn_direction = position / abs(position)

        # vitesse selon stabilité
        if abs(steer) < 0.2:
            control.move(const.mid_speed)
        else:
            control.move(const.low_speed)
        control.turn(steer)
