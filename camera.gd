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
		if packet.size() < 3:
			return

		var header = packet.slice(0, 3).get_string_from_ascii()
		var payload = packet.slice(3, packet.size())

		match header:
			"IMG":
				var image = _decode_image(payload)
				if image:
					texture = ImageTexture.create_from_image(image)
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
