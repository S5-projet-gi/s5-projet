extends CharacterBody3D

const VEHICLE_SPEED = 20.0
const WHEELBASE = 10
const LOCAL_FORWARD = Vector3.LEFT


func _physics_process(delta: float) -> void:
	if Network.is_network_connected():
		# Récupère les valeurs réseau
		var velocity_input: float = Network.data_to_send.get("velocity", 0.0)
		var direction_input = deg_to_rad(Network.data_to_send.get("direction", 0.0))

		# Convention locale du modèle: avance = vitesse négative.
		var signed_speed = -velocity_input * VEHICLE_SPEED

		# Bicycle model: yaw_rate = v / L * tan(delta)
		if abs(signed_speed) > 0.001 and abs(direction_input) > 0.001:
			rotate_y((signed_speed / WHEELBASE) * tan(direction_input) * delta)

		var heading = (global_transform.basis * LOCAL_FORWARD).normalized()
		velocity = heading * signed_speed

		# Déplacement avec collisions
		move_and_slide()
	else:
		# Stop le mouvement quand non connecté
		velocity = Vector3.ZERO
