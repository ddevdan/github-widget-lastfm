import colorsys
import requests
from haishoku.haishoku import Haishoku
from settings import LAST_FM_BASE_URL


def get_lastfm_data(user):
    url = f"{LAST_FM_BASE_URL}&user={user}"

    lastfm_response = requests.get(url).json()

    last_played_track = lastfm_response["recenttracks"]["track"][0]

    track_name, artist_name, track_cover_url = [
        last_played_track["name"],
        last_played_track["artist"]["#text"],
        last_played_track["image"][2]["#text"],
    ]

    return [track_name, artist_name, track_cover_url]


def get_colors(image_url):
    dominant = Haishoku.getDominant(
        image_path=image_url,
    )

    r, g, b = dominant
    primary = f"rgba({r}, {g}, {b}, 1)"
    secondary = f"rgba({r}, {g}, {b}, 0.8)"

    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    hue_position = int(h * 100)
    light_percent = int(l * 100)
    saturation_percent = int(s * 100)

    avarage_light = light_percent > 50
    low_light = light_percent <= 50
    high_light = light_percent >= 80
    high_saturation = saturation_percent > 80
    low_saturation = saturation_percent < 50

    text_color = f"hsl({hue_position},  {saturation_percent}%, {light_percent - 60}%)"

    if low_saturation:
        secondary = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent - 40}%)"
        )
    if low_light:
        text_color = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent + 60}%)"
        )

    elif avarage_light and high_saturation:
        secondary = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent - 40}%)"
        )
    elif high_light:
        secondary = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent - 60}%)"
        )

    primary_color = f"--primary: {primary};"
    secondary_color = f"--secondary: {secondary};"
    text_color = f"--text-color: {text_color};"

    return primary_color, secondary_color, text_color


def get_html_string(colors=[], track_info=[], title=""):
    track_name, artist_name, track_cover_url = track_info
    primary_color, secondary_color, text_color = colors

    if title:
        title = f"<h1>{title}</h1>"
    else:
        title = ""

    return (
        """<style>
        html{
       """
        + f"""
        {primary_color}
        {secondary_color}
        {text_color}
       """
        + """
        }

    </style>
    <div class="player-wrapper">"""
        + title
        + """
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
</div>

    </div>"""
    )
