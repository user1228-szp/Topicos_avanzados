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


def songs_saved(canciones):
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

    songs = canciones

    if artista:
        songs = [
            song for song in canciones
            if artista.lower() in song["artista"].lower()
        ]

    return jsonify({"canciones": songs})

@app.get("/canciones/<int:song_id>")
def get_cancion_por_id(song_id):
    cancion = busqueda_canciones(song_id)

    if cancion is None:
        abort(404, description="Canción no encontrada")

    return jsonify(cancion)

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
    songs_saved(songs)

    return jsonify(nueva_cancion), 201

@app.put("/canciones/<int:song_id>")
def update_songs(song_id):
    data = request.get_json()

    if not data:
        return jsonify({"mensaje": "No hay datos de la canción"}), 400

    songs = cargar_canciones()
    datos_obligatorios = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for i, cancion in enumerate(songs):

        if cancion["id"] == song_id:
            for campo in datos_obligatorios:
                if campo not in data:
                    return jsonify({ "mensaje": f"Falta el campo obligatorio: {campo}"}), 400

            update_song = {
                "id": song_id,
                "title": data["title"],
                "artista": data["artista"],
                "album": data["album"],
                "year": data["year"],
                "genero": data["genero"],
                "duration": data["duration"]
            }

            songs[i] = update_song
            songs_saved(songs)

            return jsonify({
                "mensaje": "Canción actualizada",
                "cancion": update_song
            }), 200

    abort(404, description="Canción no encontrada")

@app.patch("/canciones/<int:song_id>")
def patch_song(song_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "mensaje": "No hay datos de la canción"
        }), 400

    songs = cargar_canciones()

    datos_permitidos = [
        "title",
        "artista",
        "album",
        "year",
        "genero",
        "duration"
    ]

    for dato in data:
        if dato not in datos_permitidos:
            return jsonify({"mensaje": f"Campo no permitido: {dato}"}), 400

    for song in songs:
        if song["id"] == song_id:
            song.update(data)
            songs_saved(songs)

            return jsonify({"mensaje": "Canción actualizada parcialmente","cancion": song }), 200

    abort(404, description="Canción no encontrada")


@app.delete("/canciones/<int:song_id>")
def delete_song(song_id):
    songs = cargar_canciones()

    for i, song in enumerate(songs):
        if song["id"] == song_id:
            deleted_song = songs.pop(i)
            songs_saved(songs)
            return jsonify({"mensaje": "Canción eliminada", "cancion": deleted_song}), 200

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