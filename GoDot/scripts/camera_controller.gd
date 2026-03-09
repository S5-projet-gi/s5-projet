extends Camera3D

var speed = 10

func _process(delta):
    var dir = Vector3.ZERO
    
    if Input.is_key_pressed(KEY_W):
        dir.z -= 1
    if Input.is_key_pressed(KEY_S):
        dir.z += 1
    if Input.is_key_pressed(KEY_A):
        dir.x -= 1
    if Input.is_key_pressed(KEY_D):
        dir.x += 1
        
    translate(dir * speed * delta)
