extends CharacterBody3D

const VEHICLE_SPEED = 30.0
const ROTATION_SPEED = 2.0

# Variables réseau
var current_velocity := 0.0
var current_steer_dir := 0.0

func _physics_process(delta: float) -> void:
	if Network.is_network_connected():
		# Récupère les valeurs réseau
		current_velocity = Network.data_to_send.get("velocity", 0.0)
		current_steer_dir = Network.data_to_send.get("direction", 0.0)
		
		# Rotation accumulée (comme avant)
		rotation.y += -current_steer_dir * ROTATION_SPEED * delta

		# Déplacement local (comme avant)
		var move_direction = Vector3.ZERO
		move_direction.x = current_velocity * VEHICLE_SPEED
		
		# Transformer le mouvement local en mouvement global et le mettre en velocity
		var global_move_dir = transform.basis * move_direction
		velocity.x = global_move_dir.x
		velocity.z = global_move_dir.z
		
		print("DEBUG move_dir=", move_direction, " global=", global_move_dir, " velocity=", velocity, " rot=", rotation.y)
		
		# Déplacement avec collisions
		move_and_slide()
	else:
		# Stop le mouvement quand non connecté
		velocity = Vector3.ZERO
