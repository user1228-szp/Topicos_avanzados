from flask import Flask, jsonify, request, abort
import json
from pathlib import Path

import pandas as pd

app = Flask(__name__)
df = pd.read_csv("spotify_songs.csv")


def cargar_canciones():
    ruta_datos = Path(__file__).parent / "data" / "songs.json"
    with open(ruta_datos, "r") as f:
        return json.load(f)

canciones = cargar_canciones()
songs = canciones
print(canciones)


def guardar_canciones(canciones):
    ruta_datos = Path(__file__).parent / "data" / "songs.json"

    with open(ruta_datos, "w", encoding="utf-8") as f:
        json.dump(canciones, f, indent=4, ensure_ascii=False)

def busqueda_canciones(id):
    songs = cargar_canciones()
    for song in songs:
        if song["id"] == id:
            return song
    return None


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "mensaje": "API de Spotify"
    })
    

@app.route("/working")
def health():
    return jsonify({"status": "ok", "entorno": "Funcionando correctamente"})

@app.get("/canciones")
def listar_canciones():
    artista = request.args.get("artista")
    print(artista)
    return jsonify({"canciones": []})

@app.post("/canciones")
def crear_cancion():
    songs = cargar_canciones()
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "mensaje": "No se recibieron datos"
        }), 400

    campos_obligatorios = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for dato in campos_obligatorios:
        if dato not in data:
            return jsonify({
                "status": "error",
                "mensaje": f"Falta el campo obligatorio: {dato}"
            }), 400

    nuevo_id = max(cancion["id"] for cancion in songs) + 1

    nueva_cancion = {
        "id": nuevo_id,
        "title": data["title"],
        "artista": data["artista"],
        "album": data["album"],
        "year": data["year"],
        "genero": data["genero"],
        "duration": data["duration"]
    }

    songs.append(nueva_cancion)
    guardar_canciones(songs)

    return jsonify(nueva_cancion), 201


@app.put("/canciones/<int:song_id>")
def update_songs(id):
    data = request.get_json()

    if not data:
        return jsonify({"mensaje": "No hay cancion"}), 400 

    for i, cancion in enumerate(canciones):
        if cancion["id"] == id:
            datos_obligatorios = ["titulo", "artista", "album", "year", "genero", "duration"]

            for campo in datos_obligatorios:
                if campo not in data:
                    return jsonify({"mensaje": f"Falta el campo obligatorio: {campo}"}), 400

                updates_song = {
                    "id": id,
                    "titulo": data["titulo"],
                    "artista": data["artista"],
                    "album": data["album"],
                    "year": data["year"],
                    "genero": data["genero"],
                    "duration": data["duration"]
                }

                songs[i] = updates_song
                guardar_canciones(songs)

                return jsonify({"mensaje": "Canción actualizada", "cancion": updates_song}), 200
            abort(404, description="Canción no encontrada") 



@app.route("/songs/<int:song_id>")
def getSongById(song_id):
    songs = buscar_cancion_por_id(song_id)
    if songs is None:
        abort(404, description="Canción no encontrada")
    return jsonify(songs)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": e.description}), 404


@app.route("/songs")
def getSongs():
    df_proc = df.copy()
    artist = request.args.get("track_artist") #By artist
    if artist:
        df_proc = df_proc[df_proc["track_artist"].str.contains(artist)]

    song_name = request.args.get("track_name")
    if song_name:
        df_proc = df_proc[df_proc["track_name"].str.contains(song_name)]

    popularity = request.args.get("track_popularity") #By popularity
    if popularity:
        df_proc = df_proc[df_proc["track_popularity"] == int(popularity)]

    top_songs = int(request.args.get("limit") or 10)
    df_proc = df_proc.head(top_songs)

    return jsonify(df_proc.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)