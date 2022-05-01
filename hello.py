import imgkit
from flask import Flask, make_response, send_file

app = Flask(__name__)

options = {"width": 300}

@app.route("/")
def hello_world():
    image = imgkit.from_string("<h2>Hello</h3>", False, options=options)
    response = make_response(image)
    response.headers.set('Content-Type', 'image/png')
    # response.headers.set(
    #     'Content-Disposition', 'attachment', filename='image.png')
    return response
    
    # return send_file("image", attachment_filename=image mimetype='image/png')
