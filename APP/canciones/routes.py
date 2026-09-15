from flask import Blueprint, abort, jsonify, request
from pathlib import Path
from canciones import servicio
import json

canciones_bp = Blueprint("canciones", __name__, url_prefix="/canciones")



@canciones_bp.get("")
def listar_canciones():
    artista = request.args.get("artista")
    canciones = servicio.listar_canciones(artista)
    return jsonify({"canciones": canciones}), 200



@canciones_bp.post("")
def crear_cancion():
    datos = request.get_json()
    if not datos or "title" not in datos or "artista" not in datos:
        return jsonify({"status": "error", "mensaje": "Faltan campos obligatorios"}), 400
    nueva_cancion = servicio.crear_cancion(datos)
    return jsonify({"mensaje": "creation successful", "cancion": nueva_cancion}), 201


@canciones_bp.get("/<int:song_id>")
def obtener_cancion(song_id):
    cancion = servicio.busqueda_canciones(id)
    if cancion is None:
        abort(404, description="Canción no encontrada")
    return jsonify({"cancion": cancion}), 200