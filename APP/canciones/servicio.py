#Logica de negocio para manejo de canciones

import json

from pathlib import Path 

Ruta_datos = Path(__file__).resolve().parent.parent / "data" / "songs.json"


def cargar_canciones():
    with open(Ruta_datos, "r", encoding="utf-8") as f:
        return json.load(f)

canciones = cargar_canciones()
print("canciones cargadas exitosamente :)")

def songs_saved(canciones):
    ruta_datos = Path(__file__).parent.parent / "data" / "songs.json"

    with open(ruta_datos, "w", encoding="utf-8") as f:
        json.dump(
            canciones,
            f,
            indent=4,
            ensure_ascii=False
        )

def listar_canciones(artista=None):
    if artista is None:
        return canciones
    return [cancion for cancion in canciones if cancion["artista"].lower() == artista.lower()]


def busqueda_canciones(id):
    for cancion in canciones:
        if cancion["id"] == id:
            return cancion
    return None

def crear_cancion(datos):
    canciones = cargar_canciones()
    nuevo_id = max(cancion["id"] for cancion in canciones) + 1 if canciones else 1
    nueva_cancion = {
        "id": nuevo_id,
        "title": datos["title"],
        "artista": datos["artista"],
        "album": datos["album"],
        "year": datos["year"],
        "genero": datos["genero"],
        "duration": datos["duration"]
    }
    canciones.append(nueva_cancion)
    return nueva_cancion


def actualizar_cancion(song_id, data):
    songs = cargar_canciones()
    campos_obligatorios = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for i, cancion in enumerate(songs):
        if cancion["id"] == song_id:
            for campo in campos_obligatorios:
                if campo not in data:
                    return None, (
                        f"Falta el campo obligatorio: {campo}")

            cancion_actualizada = {
                "id": song_id,
                "title": data["title"],
                "artista": data["artista"],
                "album": data["album"],
                "year": data["year"],
                "genero": data["genero"],
                "duration": data["duration"]
            }
            songs[i] = cancion_actualizada
            songs_saved(songs)
            return cancion_actualizada, None

    return None, "Canción no encontrada"

def actualizar_parcial(song_id, data):
    songs = cargar_canciones()

    campos_permitidos = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for campo in data:
        if campo not in campos_permitidos:
            return None, f"Campo no permitido: {campo}"
    for song in songs:
        if song["id"] == song_id:
            song.update(data)
            songs_saved(songs)
            return song, None
    return None, "Canción no encontrada"

def eliminar_cancion(song_id):
    songs = cargar_canciones()
    for i, song in enumerate(songs):
        if song["id"] == song_id:
            deleted_song = songs.pop(i)
            songs_saved(songs)
            return deleted_song
    return None