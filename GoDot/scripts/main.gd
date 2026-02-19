extends Node3D

@onready var le_ip_address: LineEdit = $GridContainer/le_IpAdress
@onready var btn_connect: Button = $GridContainer/btn_Connect
@onready var lb_status: Label = $GridContainer/lb_ConnectionStatusPackets

func _ready() -> void:
	Network.status_changed.connect(_on_network_status_changed)
	Network.state_changed.connect(_on_network_state_changed)

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
