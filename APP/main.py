from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)


df = pd.read_csv("spotify_songs.csv")


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "mensaje": "API de Spotify"
    })
    

@app.route("/working")
def health():
    return jsonify({"status": "ok", "entorno": "Funcionando correctamente"})


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