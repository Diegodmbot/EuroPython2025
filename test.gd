extends Node


# Called when the node enters the scene tree for the first time.
func _ready():
	var output = []
	var exit_code = OS.execute("ls", ["-l"], output)
	print(output)
	print(exit_code)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
