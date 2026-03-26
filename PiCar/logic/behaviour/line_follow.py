from typing import TYPE_CHECKING

import const
from logic.behaviour.models import Movement, Sensors

if TYPE_CHECKING:
    from logic.behaviour.fsm import BehaviourFSM


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
        sensors: Sensors,
        fsm: "BehaviourFSM",
    ) -> Movement | None:
        if (
            sensors.distance > 0
            and sensors.distance <= const.wall_avoidance["trigger_distance"]
        ):
            if fsm.to_wall_avoidance():
                print(f"[Logic] Wall avoidance triggered! distance={sensors.distance}")

        active_line = [i - 2 for i in range(5) if sensors.line[i]]

        # -------------------------
        # Cas spécial : tous actifs = FIN DE COURSE
        # -------------------------
        if len(active_line) == 5:
            print("[LineFollower] ALL SENSORS ACTIVE - FINISHED!")
            fsm.to_standby()
            return

        # -------------------------
        # Cas : aucun capteur
        # -------------------------
        if not active_line:
            if self.last_turn_direction != 0:
                print(
                    f"[LineFollower] LOST - last turn direction={self.last_turn_direction}"
                )
                fsm.to_sharp_turn(self.last_turn_direction)
                return None

            print(f"[LineFollower] LOST - moving forward: {active_line}")
            return Movement(const.line_follower["med_speed"], 0)

        # position moyenne de la ligne
        position = sum(active_line) / len(active_line)
        # print(f"[LineFollower] active={active}, position={position:.2f}")
        # normalisation entre -1 et 1
        if position == -2 or position == 2:
            steer = position / 2 * const.line_follower["max_turn_angle"]
        else:
            steer = position / 2 * const.line_follower["med_turn_angle"]

        if position != 0:
            self.last_turn_direction = position / abs(position)

        # vitesse selon stabilité
        if abs(steer) < 0.2:
            return Movement(const.line_follower["max_speed"], steer)
        else:
            return Movement(const.line_follower["med_speed"], steer)
