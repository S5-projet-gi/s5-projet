extends Node3D

@onready var le_ip_address: LineEdit = $GridContainer/le_IpAdress
@onready var btn_connect: Button = $GridContainer/btn_Connect
@onready var lb_status: Label = $GridContainer/lb_ConnectionStatusPackets
@export_file var level_path

var vehicle_body: Node3D = null
var current_velocity: float = 0.0
var current_steer_dir: float = 0.0
const VEHICLE_SPEED = 30.0
const ROTATION_SPEED = 2.0

func _ready() -> void:
	Network.status_changed.connect(_on_network_status_changed)
	Network.state_changed.connect(_on_network_state_changed)
	
	# Find the vehicle body to control recursively
	vehicle_body = _find_vehicle_body()
	print("Vehicle body found: ", vehicle_body)
	
	print("Allo")

func _find_vehicle_body() -> Node3D:
	# Try to find pycar by name first
	var pycar = get_tree().current_scene.get_node_or_null("pycar")
	if pycar:
		return pycar
	
	print("No pycar found!")
	return null

func _process(delta: float) -> void:
	if Network.is_network_connected():
		if vehicle_body == null:
			print("DEBUG: vehicle_body is null")
			return
			


func _on_quit_pressed() -> void:
	Network.disconnect_network()
	get_tree().quit()

func _on_connect_pressed() -> void:
	if btn_connect.text == "Disconnect":
		Network.disconnect_network()
		return

	btn_connect.disabled = true
	Network.connect_to_ip(le_ip_address.text)
	
func _on_check_box_toggled(toggled_on: bool) -> void:
	le_ip_address.editable = !toggled_on
	if toggled_on:
		le_ip_address.text = "127.0.0.1"
		Network.set_localhost()

func _on_network_status_changed(text: String) -> void:
	lb_status.text = text
	if text == "Connected!":
		btn_connect.disabled = false
		btn_connect.text = "Disconnect"
	elif text == "Disconnected":
		btn_connect.disabled = false
		btn_connect.text = "Connect"
	elif text == "Wrong IP Address!":
		btn_connect.disabled = false

func _on_network_state_changed(state: Network.NetworkState) -> void:
	# Keep UI in sync with internal state if needed later
	pass
	
func _on_btn_next_lv_pressed() -> void:
	if level_path == null:
		return
	get_tree().change_scene_to_file(level_path)
	#"res://level_2.tscn"
