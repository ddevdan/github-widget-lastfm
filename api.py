from flask import Flask, make_response
from haishoku.haishoku import Haishoku
import requests
import imgkit
import colorsys

app = Flask(__name__)

LASTFM_BASEURL = "https://ws.audioscrobbler.com/2.0/?api_key=e013df5bf0cf898c1ac134cee9cf1ce7&method=user.getrecenttracks&format=json"

options = {
    "format": "png",
    "width": 250,
}


@app.route("/")
def hello_world():
    user = "oieusouodan"
    url = LASTFM_BASEURL + f"&user={user}"
    lastfm_response = requests.get(url).json()
    last_played_track = lastfm_response["recenttracks"]["track"][0]
    track_name = last_played_track["name"]
    artist_name = last_played_track["artist"]["#text"]
    track_cover_url = last_played_track["image"][2]["#text"]

    dominant = Haishoku.getDominant(
        image_path=track_cover_url,
    )
    r, g, b = dominant
    primary = f"rgb({r}, {g}, {b});"
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue_position = int(h * 100)
    light_percent = int(l * 100)
    saturation_percent = int(s * 100)
    print(hue_position, light_percent, saturation_percent)

    text_color = f"hsl({hue_position},  {saturation_percent}%, {light_percent - 60}%)"
    if light_percent < 50:
        text_color = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent + 60}%)"
        )

    primary_color = f"--primary: {primary}"
    text_color = f"--text-color: {text_color}"

    image = imgkit.from_string(
        """<style>
        body {margin-left:-5px;}
        html{padding:0 10px;
       """
        f"""
        {primary_color}
        {text_color}
       """
        + """
        }

    </style>
    <div class="player">
        <div class="player__music">"""
        + f"""
            <div class="player__music__image">
                <img src="{track_cover_url}" alt="{track_name} cover" /> 
            </div>
             <div class="player__music__infos">
                <p class="player__music__name">{track_name}</p>
                <p class="player__music__artist">{artist_name}</p>
            </div>
            """
        + """
           
        </div>


    </div>""",
        False,
        options=options,
        css="./index.css",
    )

    response = make_response(image)
    response.headers.set("Content-Type", "image/png")
    return response
