extends Control

var server: UDPServer
@onready var camera = $Camera
@onready var face_mask = %FaceMask

func _ready():
	server = UDPServer.new()
	server.listen(4242)

func _process(delta):
	server.poll()
	if server.is_connection_available():
		var peer: PacketPeerUDP = server.take_connection()
		var packet = peer.get_packet()
		if packet.size() < 4:
			return

		var header = packet.slice(0, 3).get_string_from_ascii()
		var payload = packet.slice(3, packet.size())

		match header:
			"IMG":
				var image = _decode_image(payload)
				if image:
					camera.texture = ImageTexture.create_from_image(image)
			"REC":
				var coords = payload.get_string_from_utf8().split(",")
				var x = float(coords[0])
				var y = float(coords[1])
				var w = float(coords[2])
				var h = float(coords[3])
				face_mask.position = Vector2(x, y)
				face_mask.size = Vector2(x+w,y+h)
			"TXT":
				var message = payload.get_string_from_utf8()
				print("Mensaje recibido:", message)
			_:
				print("Tipo desconocido:", header)

func _decode_image(frame_data: PackedByteArray) -> Image:
	var image = Image.new()
	var success = image.load_jpg_from_buffer(frame_data)
	if success != OK:
		print("Error al cargar imagen")
		return null
	return image
