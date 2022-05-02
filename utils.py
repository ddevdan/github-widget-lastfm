import colorsys
import requests
from haishoku.haishoku import Haishoku


LASTFM_BASEURL = "https://ws.audioscrobbler.com/2.0/?api_key=e013df5bf0cf898c1ac134cee9cf1ce7&method=user.getrecenttracks&format=json"


def get_lastfm_data(user):
    url = f"{LASTFM_BASEURL}&user={user}"

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
    primary = f"rgb({r}, {g}, {b});"

    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    hue_position = int(h * 100)
    light_percent = int(l * 100)
    saturation_percent = int(s * 100)

    text_color = f"hsl({hue_position},  {saturation_percent}%, {light_percent - 60}%)"
    if light_percent < 50:
        text_color = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent + 60}%)"
        )

    primary_color = f"--primary: {primary}"
    text_color = f"--text-color: {text_color}"
    return primary_color, text_color


def get_html_string(colors=[], track_info=[]):
    track_name, artist_name, track_cover_url = track_info
    primary_color, text_color = colors

    return (
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


    </div>"""
    )
