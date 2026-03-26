picar = {
    "max_turn_angle": 45,  # degrees
    "wheelbase": 14,  # centimeters
    "wheel_spacing": 11,  # centimeters
    "wheel_diameter": 6.5,  # centimeters
    "debug": False,
}

two_point_turn = {
    "distance": picar["wheelbase"] * 2.2,
    "turn_angle": picar["max_turn_angle"],
}

wall_avoidance = {
    "trigger_distance": 3,
    "first_speed": -0.1,
    "first_time": 2,
    "first_angle": 45,
    "second_speed": 0.1,
    "second_time": 2,
    "second_angle": 0,
    "third_speed": 0.1,
    "third_time": 2,
    "third_angle": 45,
}


max_speed: float = 0.1
mid_speed: float = 0.1
low_speed: float = 0.1
accel_rate: float = 1.2

line_follower_med_turn_angle: float = 60
line_follower_max_turn_angle: float = 75

dir_buffer_size: int = 16
