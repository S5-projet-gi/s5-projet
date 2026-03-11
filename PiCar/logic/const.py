max_speed: float = 0.1
mid_speed: float = 0.1
low_speed: float = 0.1
accel_rate: float = 1.2

line_follower_med_turn_angle: float = 40
line_follower_max_turn_angle: float = 70

dir_buffer_size: int = 16

# Wall avoidance parameters
wall_avoid_detection_distance: float = 3.0  # Distance threshold to trigger avoidance
wall_avoid_rotation_angle: float = 85  # Angle to turn when avoiding (radians)
wall_avoid_forward_distance: float = 0.3  # Distance to travel after turning
wall_avoid_turn_speed: float = 0.05  # Speed when turning to avoid wall
wall_avoid_forward_speed: float = 0.1  # Speed when moving forward to avoid wall
