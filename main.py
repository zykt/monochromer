"""
##################################################################
Simple web server to get an image from user and make it monochrome
##################################################################
"""
from flask import Flask, render_template, request
from enum import Enum
import os
from multiprocessing import Process
from monochromer import convert


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.curdir, 'image')


# AppStatus = Enum('AppStatus', ['idle', 'processing', 'ready'])
class AppStatus(Enum):
    idle = 0
    processing = 1
    ready = 2

app_status = AppStatus.idle

status_strings = {
    AppStatus.idle: "Send an image to process!",
    AppStatus.processing: "Processing...",
    AppStatus.ready: "Your image is ready!",
}


def greyscale(*args):
    """
    wrapper around monochrome.convert with app_status sideeffects
    """
    global app_status
    app_status = AppStatus.processing
    convert(*args)
    app_status = AppStatus.ready


@app.route("/")
def main():
    """Main page"""
    return render_template('main.html')


@app.route("/image", methods=['GET', 'POST'])
@app.route("/imagegoeshere", methods=['GET', 'POST'])
def image():
    """Image goes here"""
    # TODO: handle errors!
    if request.method == 'POST':
        f = request.files['imagefile']
        _, file_ext = os.path.splitext(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f'image{file_ext}')
        output = os.path.join(app.config['UPLOAD_FOLDER'], f'output{file_ext}')
        f.save(filepath)
        print('Got an image', f.filename)
        # TODO: FIX! syncing back to main thread (app_status)
        p = Process(target=greyscale, args=(filepath, output))
        p.start()
        p.join()
        # TODO: delete after use
        return render_template('image.html', imagename=f.filename, file_ext=file_ext)
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
