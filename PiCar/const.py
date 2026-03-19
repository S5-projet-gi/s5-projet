picar = {
    "max_turn_angle": 45,  # degrees
    "wheelbase": 14,  # centimeters
    "wheel_spacing": 11,  # centimeters
    "wheel_diameter": 6.5,  # centimeters
}

two_point_turn = {
    "distance": picar["wheelbase"] * 2.2,
    "turn_angle": picar["max_turn_angle"],
}


max_speed: float = 0.1
mid_speed: float = 0.1
low_speed: float = 0.1
accel_rate: float = 1.2

line_follower_med_turn_angle: float = 60
line_follower_max_turn_angle: float = 75

dir_buffer_size: int = 16

# Wall avoidance parameters
wall_avoid_detection_distance: float = 3.0  # Distance threshold to trigger avoidance
wall_avoid_rotation_angle: float = 85  # Angle to turn when avoiding (radians)
wall_avoid_forward_distance: float = 0.3  # Distance to travel after turning
wall_avoid_turn_speed: float = 0.05  # Speed when turning to avoid wall
wall_avoid_forward_speed: float = 0.1  # Speed when moving forward to avoid wall
