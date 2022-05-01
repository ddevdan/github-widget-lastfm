from io import BytesIO
from random import randint
from turtle import width
import imgkit
from flask import Flask, make_response, request, send_file
from PIL import Image
from haishoku.haishoku import Haishoku
import colorsys


import requests

app = Flask(__name__)

LASTFM_BASEURL = "https://ws.audioscrobbler.com/2.0/?api_key=e013df5bf0cf898c1ac134cee9cf1ce7&method=user.getrecenttracks&format=json"

options = {"format": "png", "disable-smart-width": ""}


@app.route("/")
def hello_world():
    value = randint(0, 9)
    user = "oieusouodan"
    url = LASTFM_BASEURL + f"&user={user}"
    lastfm_response = requests.get(url).json()
    last_played_track = lastfm_response["recenttracks"]["track"][value]
    track_name = last_played_track["name"]
    artist_name = last_played_track["artist"]["#text"]
    track_cover_url = last_played_track["image"][2]["#text"]
    # print(track_cover_url)
    track_cover_big_url = last_played_track["image"][3]["#text"]
    track_cover_response = requests.get(track_cover_url)
    track_cover_image = track_cover_response.content
    im = Image.open(requests.get(track_cover_url, stream=True).raw)

    # print("palette =>", im.getpalette())
    im2 = im.convert("P", palette=Image.ADAPTIVE, colors=256)
    # print(im2.getcolors())
    # print(im2.palette)
    # dominant = Haishoku.getDominant(im2.palette)
    # palette = Haishoku.loadHaishoku( track_cover_image )
    # haishoku = Haishoku.loadHaishoku(track_cover_url)

    dominant = Haishoku.getDominant(
        image_path=track_cover_url,
    )
    r, g, b = dominant
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    hue_position = int(h * 100)
    light_percent = int(l * 100)
    saturation_percent = int(s * 100)
    print(hue_position, light_percent, saturation_percent)
    # print("r,g,b => ", r, g, b)
    # print("h, l, s => ", h, l, s)
    text_color = f"hsl({hue_position},  {saturation_percent}%, {light_percent - 60}%)"
    if light_percent < 50:
        text_color = (
            f"hsl({hue_position},  {saturation_percent}%, {light_percent + 60}%)"
        )

    # dominant_hsl = colorsys.rgb_to_hls(r=r, g=g, b=b)
    palette = Haishoku.getPalette(image_path=track_cover_url)
    # dominant = Haishoku.getDominant(
    #     image_path="https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Red_flag.svg/1280px-Red_flag.svg.png"
    # )
    # print("dominant_hsl => ", dominant_hsl)
    # print(f"background-color: {dominant};")
    image = imgkit.from_string(
        #     f""" <div>
        #     <h1>
        #         last played music
        #     </h1>
        #     <img src="{track_cover}" alt="{track_name} cover" />
        #     <h3>artist - {artist_name} </h3>
        #     <h3>music - {track_name} </h3>
        # </div>
        # """,
        """<style>
        html,
        body{
            background: rgba(0,0,0,0);
        }
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;700&display=swap');

         .player {
            width: 300px;
            height: auto;
            border-radius: 15px;
            font-family: 'Poppins', sans-serif;
            display: flex;
            align-items: center;
                padding: 5px;
                
                """
        + f"""background-color: rgb{dominant};
        border:2px solid rgb{dominant};"""
        + """
        }

        .player__music {
            display: flex;
            justify-content: flex-start;
            align-items: center;

            font-family: 'Poppins', sans-serif;
        }

 .player__music__image {
            line-height: 0;
        }

        .player__music__infos {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: center;
            gap: 0;
            margin-left:15px;
        }

        .player__music__infos p {
            margin: 0;
            padding: 0;
            line-height: 18px;
            """
        f"color: {text_color};"
        """
        }

        .player__music__infos p:first-of-type {
            font-weight: bold;
        }

        img {
            height: 50px;
            line-height: 0;
            margin: -5px;
            border-radius: 10px 5px 5px 10px;
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
        <!-- <progress /> -->


    </div>""",
        False,
        options=options
        # options=options,
    )

    # print(track_name, artist_name)
    response = make_response(image)
    response.headers.set("Content-Type", "image/png")
    # response.headers.set(
    #     'Content-Disposition', 'attachment', filename='image.png')
    return response

    # return send_file("image", attachment_filename=image mimetype='image/png')
