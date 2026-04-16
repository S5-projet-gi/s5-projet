picar = {
    "max_turn_angle": 45,  # degrees
    "wheelbase": 14,  # centimeters
    "wheel_spacing": 11,  # centimeters
    "wheel_diameter": 6.5,  # centimeters
    "debug": False,
    "distance_rate": 20,
    "angle_accel_rate": 50.0,
    "speed_accel_rate": 35.0,
}

two_point_turn = {
    # Avancer plus loin que la ligne
    "first_distance": picar["wheelbase"] * 1.2,
    "first_speed": 30,
    "first_angle": 0,
    # Tourner à 90 degrés
    "second_distance": picar["wheelbase"] * 3.5,
    "second_speed": -30,
    "second_angle": picar["max_turn_angle"],
}

wall_avoidance = {
    # Reculer en tournant
    "trigger_distance": 25,
    "first_speed": -30,
    "first_time": 65,
    "first_angle": 40,
    # Avancer
    "second_speed": 30,
    "second_time": 115,
    "second_angle": 5,
    # Avancer en tournant pour retourner la ligne
    "third_speed": 30,
    "third_angle": 35,
    # Tourner de l'autre côté pour s'enligner
    "fourth_speed": 20,
    "fourth_time": 12,
    "fourth_angle": -picar["max_turn_angle"],
}

line_follower = {
    "black_threshold": 130,  # 130 on white
    "gray_threshold": 110,  # 110 on white
    "med_turn_angle": 8,
    "med_turn_speed": 40,
    "max_turn_angle": 35,
    "max_turn_speed": 35,
    "lost_angle": picar["max_turn_angle"],
}
