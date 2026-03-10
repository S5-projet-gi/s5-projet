extends Node

# Global websocket manager (autoload singleton)
enum NetworkState { WAITING, INIT, CONNECTING, PROCESS, CLOSING }

signal state_changed(new_state: NetworkState)
signal status_changed(text: String)

# Networking
var socket: WebSocketPeer
var data_to_send = {"velocity": 0.0, "direction": 0.0}
var data_received = {"distance": 0, "line_follower": [0, 0, 0, 0, 0]}

# State
var network_state: NetworkState = NetworkState.WAITING
var send_timer := 0.0
var ip_address := "127.0.0.1"

# Validation
var network_ip_addr_regex := RegEx.new()

func _ready() -> void:
	network_ip_addr_regex.compile(r'^([01]?\d?\d|2[0-4]\d|25[0-4]).([01]?\d?\d|2[0-4]\d|25[0-4]).([01]?\d?\d|2[0-4]\d|25[0-4]).([01]?\d?\d|2[0-4]\d|25[0-4])$')

func _process(delta: float) -> void:
	_update_network_fsm(delta)

func connect_to_ip(ip: String) -> void:
	if not _is_valid_ip(ip):
		_emit_status("Wrong IP Address!")
		return

	ip_address = ip
	_emit_status("Connecting")
	_set_state(NetworkState.INIT)

func disconnect_network() -> void:
	_set_state(NetworkState.CLOSING)

func set_localhost() -> void:
	ip_address = "127.0.0.1"
	_emit_status("Connecting")
	_set_state(NetworkState.INIT)

func is_network_connected() -> bool:
	return network_state == NetworkState.PROCESS

func _update_network_fsm(delta: float) -> void:
	match network_state:
		NetworkState.WAITING:
			# Idle, waiting for user input
			pass

		NetworkState.INIT:
			# Reuse existing socket across reconnects
			if socket == null:
				socket = WebSocketPeer.new()
			else:
				# Ensure any previous session is closed before reconnecting
				if socket.get_ready_state() == WebSocketPeer.STATE_OPEN:
					socket.close(1000, "Reconnecting")
			socket.connect_to_url("ws://" + ip_address + ":8765")
			_set_state(NetworkState.CONNECTING)

		NetworkState.CONNECTING:
			if socket == null:
				_set_state(NetworkState.INIT)
				return

			# Poll first, then check readiness
			socket.poll()
			if socket.get_ready_state() == WebSocketPeer.STATE_CONNECTING:
				pass
			elif socket.get_ready_state() == WebSocketPeer.STATE_OPEN:
				_emit_status("Connected!")
				_set_state(NetworkState.PROCESS)
			elif socket.get_ready_state() == WebSocketPeer.STATE_CLOSED or socket.get_ready_state() == WebSocketPeer.STATE_CLOSING:
				_set_state(NetworkState.INIT)

		NetworkState.PROCESS:
			if socket == null:
				_set_state(NetworkState.INIT)
				return

			socket.poll()
			var state := socket.get_ready_state()
			if state == WebSocketPeer.STATE_OPEN:
				# Receive packets
				while socket.get_available_packet_count() > 0:
					data_received = JSON.parse_string(socket.get_packet().get_string_from_utf8())
					print(data_received)
					if data_received == null:
						print("Error while parsing received string")
					if data_received.get("type") == "control":
						data_to_send["velocity"] = data_received.get("speed", 0.0)
						data_to_send["direction"] = data_received.get("steer_dir", 0.0)
						print("Received control: speed=", data_to_send["velocity"], " steer_dir=", data_to_send["direction"])

				# Send data every ~50ms
				if send_timer > 0.05:
					var picar_raycast = get_tree().current_scene.get_node_or_null("Ultrasonic")
					var distance = 100
					if picar_raycast and picar_raycast.has_method("get_distance"):
						distance = picar_raycast.get_distance()
					
					var line_follower_node = _get_line_follower_node()
					var line_follower_array = [0, 0, 0, 0, 0]
					if line_follower_node:
						line_follower_array = line_follower_node.get_line_follower_array()
					
					var json_data = JSON.stringify({ "type": "sensor", "data": { "line_follower": line_follower_array, "distance": distance }}).to_utf8_buffer()
					print("GODOT SENDING: type=sensor, line_follower=", line_follower_array, " distance=", distance)
					socket.send(json_data)
					send_timer = 0.0
				else:
					send_timer += delta
			elif state == WebSocketPeer.STATE_CLOSING or state == WebSocketPeer.STATE_CLOSED:
				_set_state(NetworkState.CLOSING)

		NetworkState.CLOSING:
			if socket != null:
				socket.close(1000, "Connection was closed by the user")
			_emit_status("Disconnected")
			_set_state(NetworkState.WAITING)

func _set_state(next_state: NetworkState) -> void:
	if network_state == next_state:
		return
	network_state = next_state
	state_changed.emit(network_state)

func _emit_status(text: String) -> void:
	status_changed.emit(text)

func _is_valid_ip(ip: String) -> bool:
	return network_ip_addr_regex.search_all(ip).size() > 0

func _get_line_follower_node() -> Node:
	# Recherche récursive dans toute l'arborescence
	var queue = [get_tree().current_scene]
	while queue.size() > 0:
		var node = queue.pop_front()
		if node and node.has_method("get_line_follower_array"):
			return node
		if node:
			for child in node.get_children():
				queue.append(child)
	return null
