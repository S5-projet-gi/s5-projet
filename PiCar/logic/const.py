max_speed: float = 0.01
mid_speed: float = 0.01
low_speed: float = 0.01
accel_rate: float = 1.2

turn_angle_mid: float = 0.05
turn_angle_big: float = 0.03
turn_accel: float = 1

dir_buffer_size: int = 16

# Wall avoidance parameters
wall_avoid_detection_distance: float = 3.0  # Distance threshold to trigger avoidance
wall_avoid_rotation_angle: float = 0.9  # Angle to turn when avoiding (radians)
wall_avoid_forward_distance: float = 0.05  # Distance to travel after turning
wall_avoid_turn_speed: float = 0.20  # Speed when turning to avoid wall
wall_avoid_forward_speed: float = 0.15  # Speed when moving forward to avoid wall
wall_avoid_rotation_angle_bonus: float = 1.3  # Bonus multiplier for rotation angle to ensure effective avoidance


# max_speed: float = 0.1
# mid_speed: float = 0.1
# low_speed: float = 0.1
# accel_rate: float = 1.2

# turn_angle_mid: float = 0.05
# turn_angle_big: float = 0.3
# turn_accel: float = 1

# dir_buffer_size: int = 16

# # Wall avoidance parameters
# wall_avoid_detection_distance: float = 3.0  # Distance threshold to trigger avoidance
# wall_avoid_rotation_angle: float = 0.9  # Angle to turn when avoiding (radians)
# wall_avoid_forward_distance: float = 0.05  # Distance to travel after turning
# wall_avoid_turn_speed: float = 0.20  # Speed when turning to avoid wall
# wall_avoid_forward_speed: float = 0.15  # Speed when moving forward to avoid wall
# wall_avoid_rotation_angle_bonus: float = 1.3  # Bonus multiplier for rotation angle to ensure effective avoidance