extends TextureRect

var server: UDPServer

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

		var header = packet.slice(0, 4).get_string_from_ascii()
		var payload = packet.slice(4, packet.size())

		match header:
			"IMG0":
				var image = _decode_image(payload)
				if image:
					texture = ImageTexture.create_from_image(image)
			"TXT0":
				var message = payload.get_string_from_utf8()
				print("Mensaje recibido:", message)
			"VEC2":
				var coord_x = float(payload.get_string_from_utf8().get_slice(",", 0))
				var coord_y = float(payload.get_string_from_utf8().get_slice(",", 1))
				print("Recibido VEC2x:", coord_x, coord_y)
			_:
				print("Tipo desconocido:", header)

func _decode_image(frame_data: PackedByteArray) -> Image:
	var image = Image.new()
	var success = image.load_jpg_from_buffer(frame_data)
	if success != OK:
		print("Error al cargar imagen")
		return null
	return image
