"""
##################################################################
Simple web server to get an image from user and make it monochrome
##################################################################
"""
from flask import Flask, render_template, request
import os
from enum import Enum

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.curdir, 'image')


# AppStatus = Enum('AppStatus', ['idle', 'processing', 'ready'])
class AppStatus(Enum):
  idle = 1
  processing = 2
  ready = 3
app_status = AppStatus.idle

status_strings = {
    AppStatus.idle: "Send an image to process!",
    AppStatus.processing: "Processing...",
    AppStatus.ready: "Your image is ready!",
}


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/image", methods=['GET', 'POST'])
@app.route("/imagegoeshere", methods=['GET', 'POST'])
def image():
    # TODO: handle errors!
    # TODO: Add support for file formats other than png!
    if request.method == 'POST':
        f = request.files['imagefile']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], 'image.png'))
        print('Got an image', f.filename)
        return render_template('image.html', imagename=f.filename)
    else:
        return f'Errrrrror! Got {request.method}. Expected POST\n'


@app.route("/status")
def status():
    """
    return server status
    format:
    [{code}]{status_string}
    where code is a single digit representing server status
    and status_string is a string which corresponds to that server status
    [{code}] should always be 3 chars long including square brackets for ease of parsing
    """
    return f'[{app_status.value}]{status_strings[app_status]}'


app.run()
