extends Node
#
var base_dir := OS.get_executable_path().get_base_dir()
var interpreter_path := base_dir.path_join("python/venv/Scripts/python.exe")
var script_path := base_dir.path_join("python/client.py")
var python_process: Dictionary
func _ready():
	if not OS.has_feature("standalone"):
		interpreter_path = ProjectSettings.globalize_path("res://python/venv/Scripts/python.exe")
		script_path = ProjectSettings.globalize_path("res://python/client.py")
	start_python_script()

func _process(delta):
	if Input.is_action_pressed("ui_accept"):
		stop_python_script()

func start_python_script():
	python_process = OS.execute_with_pipe(interpreter_path, [script_path])
	print(python_process["pid"])

func stop_python_script():
	OS.kill(python_process["pid"])
