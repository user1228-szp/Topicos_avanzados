#Logica de negocio para manejo de canciones

import json

from pathlib import Path 

Ruta_datos = Path(__file__).resolve().parent.parent / "data" / "songs.json"


def cargar_canciones():
    with open(Ruta_datos, "r", encoding="utf-8") as f:
        return json.load(f)

canciones = cargar_canciones()
print("canciones cargadas exitosamente :)")


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