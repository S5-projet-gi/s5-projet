extends Node3D

const RAY_LENGTH = 1000.0
const NO_HIT_DISTANCE = 1000000.0

var ray: RayCast3D
var distance: float = NO_HIT_DISTANCE

func _ready():
	ray = get_node("../Ultrasonic")
	ray.target_position = Vector3(-RAY_LENGTH, 0, 0)
	ray.enabled = true

func _physics_process(_delta):
	if ray.is_colliding():
		var hit_point = ray.get_collision_point()
		distance = hit_point.distance_to(global_position)
	else:
		distance = NO_HIT_DISTANCE

func get_distance() -> float:
	return distance
