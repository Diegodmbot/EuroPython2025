#extends Node
#
#var dir := OS.get_executable_path().get_base_dir()
#var interpreter_path := dir.path_join("python/venv/bin/python3.10")
#var server_client_script_path := dir.path_join("python/client.py")
#
#func _ready():
	#if not OS.has_feature("standalone"):
		#interpreter_path = ProjectSettings.globalize_path("res://python/venv/Scripts/python.exe")
		#server_client_script_path = ProjectSettings.globalize_path("res://python/client.py")
#
	#OS.execute(interpreter_path, [server_client_script_path])
