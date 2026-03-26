picar = {
    "max_turn_angle": 45,  # degrees
    "wheelbase": 14,  # centimeters
    "wheel_spacing": 11,  # centimeters
    "wheel_diameter": 6.5,  # centimeters
    "debug": False,
}

two_point_turn = {
    # Avancer plus loin que la ligne
    "first_distance": picar["wheelbase"] * 2.2,
    "first_speed": 10,
    "first_angle": 0,

    # Tourner à 90 degrés 
    "second_distance": picar["wheelbase"] * 2.2,
    "second_speed": -10,
    "second_angle": picar["max_turn_angle"],
}

wall_avoidance = {
    "trigger_distance": 3,
    "first_speed": -10,
    "first_time": 2,
    "first_angle": 45,
    "second_speed": 10,
    "second_time": 2,
    "second_angle": 0,
    "third_speed": 10,
    "third_time": 2,
    "third_angle": 45,
}

line_follower = {
    "black_threshold": 1,
    "med_turn_angle": 10,
    "max_turn_angle": picar["max_turn_angle"],
    "med_speed": 10,
    "max_speed": 10,
}
