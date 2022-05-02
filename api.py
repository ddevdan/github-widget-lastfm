import os
from flask import Flask, make_response
import imgkit

from utils import get_colors, get_html_string, get_lastfm_data

app = Flask(__name__)


HOME = os.path.dirname(os.path.abspath(__file__))
css_file_path = os.path.join(HOME, './assets/index.css')

options = {
    "format": "png",
    "width": 250,
}


@app.route("/lastfm/generate/<username>")
def show_last_played_image(username):
    user = username

    track_name, artist_name, track_cover_url = get_lastfm_data(user)

    primary_color, secondary_color, text_color = get_colors(image_url=track_cover_url)

    html_string = get_html_string(
        track_info=[track_name, artist_name, track_cover_url],
        colors=[primary_color, secondary_color, text_color],
    )

    image = imgkit.from_string(
        html_string,
        False,
        options=options,
        css=css_file_path,
    )
    

    response = make_response(image)
    response.headers.set("Content-Type", "image/png")
    return response
