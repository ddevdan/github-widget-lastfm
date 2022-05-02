from flask import Flask, make_response
from haishoku.haishoku import Haishoku
import requests
import imgkit
import colorsys

from utils import get_colors, get_html_string, get_lastfm_data

app = Flask(__name__)


options = {
    "format": "png",
    "width": 250,
}


@app.route("/")
def generate_image():
    user = "oieusouodan"

    track_name, artist_name, track_cover_url = get_lastfm_data(user)

    primary_color, text_color = get_colors(image_url=track_cover_url)

    html_string = get_html_string(
        track_info=[track_name, artist_name, track_cover_url],
        colors=[primary_color, text_color],
    )

    image = imgkit.from_string(
        html_string,
        False,
        options=options,
        css="./templates/index.css",
    )

    response = make_response(image)
    response.headers.set("Content-Type", "image/png")
    return response
