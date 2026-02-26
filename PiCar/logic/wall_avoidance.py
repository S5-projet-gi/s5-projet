from dataclasses import dataclass


@dataclass
class WallAvoidanceLogic:
    """State for the wall avoidance controller."""

    active: bool = False
    elapsed: float = 0.0


class WallAvoidanceController:
    """
    Time-based wall avoidance sequence.

    Call `update(delta)` while `state.active` is True. It returns (speed, steer_dir, done).
    """

    def __init__(
        self,
        turn_angle_big: float = 1.0,
        low_speed: float = 0.05,
    ):
        self.turn_angle_big = turn_angle_big
        self.low_speed = low_speed
        self.state = WallAvoidanceLogic()

    def trigger(self):
        self.state.active = True
        self.state.elapsed = 0.0

    def update(self, delta: float) -> tuple[float, float, bool]:
        if not self.state.active:
            return 0.0, 0.0, True

        t = self.state.elapsed
        steer_dir = 0.0
        speed = 0.0

        # Sequence copied from GoDot logic (time windows)
        if 0.0 <= t < 1.3:
            steer_dir = self.turn_angle_big
            speed = 0.0
        elif 1.3 <= t < 2.0:
            steer_dir = 0.0
            speed = self.low_speed
        elif 2.0 <= t < 4.5:
            steer_dir = -self.turn_angle_big
            speed = 0.0
        elif 4.5 <= t < 5.0:
            steer_dir = 0.0
            speed = self.low_speed
        elif 5.0 <= t < 7.5:
            steer_dir = -self.turn_angle_big
            speed = 0.0
        elif 7.5 <= t < 8.2:
            steer_dir = 0.0
            speed = self.low_speed
        elif 8.2 <= t < 9.5:
            steer_dir = self.turn_angle_big
            speed = 0.0
        else:
            self.state.active = False
            self.state.elapsed = 0.0
            return 0.0, 0.0, True

        self.state.elapsed += delta
        return speed, steer_dir, False
