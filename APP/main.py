from flask import Flask, jsonify, request, abort
from pathlib import Path
from canciones.routes import canciones_bp

import pandas as pd
import json

app = Flask(__name__)
app.register_blueprint(canciones_bp)
df = pd.read_csv("spotify_songs.csv")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "mensaje": "API de Spotify"
    })
    

if __name__ == "__main__":
    app.run(debug=True)