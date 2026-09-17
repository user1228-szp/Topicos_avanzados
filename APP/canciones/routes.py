from flask import Blueprint, abort, jsonify, request
from canciones import servicio


canciones_bp = Blueprint(
    "canciones",
    __name__,
    url_prefix="/canciones"
)

@canciones_bp.get("")
def listar_canciones():
    artista = request.args.get("artista")
    canciones = servicio.listar_canciones(artista)
    return jsonify({"canciones": canciones}), 200

@canciones_bp.post("")
def crear_cancion():
    datos = request.get_json()
    if not datos:
        return jsonify({"status": "error","mensaje": "No se recibieron datos"}), 400

    campos_obligatorios = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for campo in campos_obligatorios:
        if campo not in datos:
            return jsonify({"status": "error","mensaje": f"Falta el campo obligatorio: {campo}"}), 400
    nueva_cancion = servicio.crear_cancion(datos)
    return jsonify({"mensaje": "creation successful","cancion": nueva_cancion}), 201

@canciones_bp.get("/<int:song_id>")
def obtener_cancion(song_id):
    cancion = servicio.busqueda_canciones(song_id)
    if cancion is None:
        abort(404, description="Canción no encontrada")
        return jsonify({"cancion": cancion}), 200

@canciones_bp.put("/<int:song_id>")
def actualizar_cancion(song_id):
    datos = request.get_json()
    if not datos:
        return jsonify({"mensaje": "No hay datos de la canción"}), 400
    cancion, error = servicio.actualizar_cancion(song_id,datos)

    if error:
        if error == "Canción no encontrada":
            abort(404, description=error)
        return jsonify({"mensaje": error}), 400

    return jsonify({"mensaje": "Song updated","cancion": cancion}), 200

@canciones_bp.patch("/<int:song_id>")
def patch_song(song_id):

    datos = request.get_json()

    if not datos:
        return jsonify({"mensaje": "No hay datos de la canción"}), 400

    cancion, error = servicio.actualizar_parcial(
        song_id,
        datos
    )

    if error:
        if error == "Canción no encontrada":
            abort(404, description=error)
        return jsonify({"mensaje": error}), 400
    return jsonify({"mensaje": "partial update","cancion": cancion}), 200

@canciones_bp.delete("/<int:song_id>")
def eliminar_cancion(song_id):
    cancion = servicio.eliminar_cancion(song_id)
    if cancion is None:
        abort(404, description="Canción no encontrada")
    return jsonify({"mensaje": "Deleted","cancion": cancion}), 200