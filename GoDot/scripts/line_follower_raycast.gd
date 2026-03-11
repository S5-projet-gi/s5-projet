extends Area3D


@export var line_follower_array: PackedByteArray = [0,0,0,0,0]

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	print("Read Line: ", line_follower_array)
	pass

func _on_body_shape_entered(body_rid, body, body_shape_index, local_shape_index):	
	# Vérifier avec bitwise AND : body doit être sur une layer que le sensor scanne
	if body.collision_layer & collision_mask:
		line_follower_array[local_shape_index] = 1


func _on_body_shape_exited(body_rid, body, body_shape_index, local_shape_index):
	if body.collision_layer & collision_mask:
		line_follower_array[local_shape_index] = 0


func _on_area_exited(area: Area3D) -> void:
	pass # Replace with function body.

func get_line_follower_array() -> PackedByteArray:
	return line_follower_array
