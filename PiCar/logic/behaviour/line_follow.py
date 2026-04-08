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
        if all([x == 2 for x in sensors.line]):
            print("[LineFollower] ALL SENSORS ACTIVE - FINISHED!")
            fsm.to_standby()
            return

        # -------------------------
        # Cas : aucun capteur
        # -------------------------
        if all([x == 0 for x in sensors.line]):
            if self.last_turn_direction != 0:
                print(
                    f"[LineFollower] LOST - last turn direction={self.last_turn_direction}"
                )
                fsm.to_sharp_turn(self.last_turn_direction)
                return None

            print(f"[LineFollower] LOST - moving forward: {sensors.line}")
            return Movement(const.line_follower["max_turn_speed"], 0)

        if sensors.line[0] == 1 and sensors.line[1] == 0:
            self.last_turn_direction = -1
            return Movement(
                const.line_follower["max_turn_speed"],
                -const.line_follower["max_turn_angle"],
            )
        if sensors.line[4] == 1 and sensors.line[3] == 0:
            self.last_turn_direction = 1
            return Movement(
                const.line_follower["max_turn_speed"],
                const.line_follower["max_turn_angle"],
            )

        angle = (
            -const.line_follower["max_turn_angle"] * sensors.line[0]
            - const.line_follower["med_turn_angle"] * sensors.line[1]
            + const.line_follower["med_turn_angle"] * sensors.line[3]
            + const.line_follower["max_turn_angle"] * sensors.line[4]
        ) / 2

        if angle != 0:
            self.last_turn_direction = angle / abs(angle)

        # vitesse selon stabilité
        if abs(angle) < 0.2:
            return Movement(const.line_follower["med_turn_speed"], angle)
        else:
            return Movement(const.line_follower["max_turn_speed"], angle)
