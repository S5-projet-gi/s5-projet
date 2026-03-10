extends Camera3D

@export var speed : float = 10.0        # vitesse de déplacement
@export var mouse_sensitivity : float = 0.003  # sensibilité de la souris

var yaw : float = 0.0
var pitch : float = 0.0

func _ready():
	# Capture la souris pour pouvoir regarder autour
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event):
	# Relâche / recapture la souris avec ESC
	if event is InputEventKey and event.pressed:
		if event.keycode == KEY_ESCAPE:
			if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
				Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
			else:
				Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	
	# Gestion du mouvement de la souris
	if event is InputEventMouseMotion:
		yaw -= event.relative.x * mouse_sensitivity
		pitch -= event.relative.y * mouse_sensitivity
		pitch = clamp(pitch, -PI/2, PI/2)
		rotation = Vector3(pitch, yaw, 0)

func _process(delta):
	_handle_movement(delta)

func _handle_movement(delta):
	var dir = Vector3.ZERO
	
	# Déplacement avec axes GLOBAUX (fixes, peu importe la rotation de la caméra)
	if Input.is_key_pressed(KEY_W):
		dir += Vector3.FORWARD
	if Input.is_key_pressed(KEY_S):
		dir -= Vector3.FORWARD
	if Input.is_key_pressed(KEY_A):
		dir -= Vector3.RIGHT
	if Input.is_key_pressed(KEY_D):
		dir += Vector3.RIGHT
	
	# Monter / descendre
	if Input.is_key_pressed(KEY_SPACE):
		dir += Vector3.UP
	if Input.is_key_pressed(KEY_SHIFT):
		dir -= Vector3.UP

	if dir != Vector3.ZERO:
		dir = dir.normalized()
		translate(dir * speed * delta)
