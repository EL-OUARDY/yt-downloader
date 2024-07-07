import os
import threading
import time
from flask import Flask, abort, jsonify, render_template, request, send_file
from pytube import YouTube

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/details")
def details():
    url = request.args.get("url")

    # check passed url
    if url is None or url == "":
        abort(400, description="Bad Request: URL is not valid")

    try:
        yt = YouTube(url)  # get youtube video
    except:
        abort(404, description="Not Found: Video not found")

    # get details about the video
    details = {
        "title": yt.title,
        "thumbnail": yt.thumbnail_url,
        "views": yt.views,
        "length": yt.length,
    }

    return jsonify(details)


@app.route("/download")
def download():
    url = request.args.get("url")

    # check passed url
    if url is None or url == "":
        abort(400, description="Bad Request: URL is not valid")

    # download video
    try:
        video_path = download_video(url)
    except Exception as e:
        abort(500, description=f"Error: Can't get the specified video. sorry!")

    # start a thread to delete the file after 1 hour (3600 seconds)
    threading.Thread(
        target=delete_file_after_time, args=(video_path, 3600)
    ).start()

    return send_file(video_path, as_attachment=True)


def download_video(url):
    yt = YouTube(url)
    stream = yt.streams.filter(
        progressive=True, file_extension="mp4"
    ).get_highest_resolution()
    video_path = stream.download("./videos")
    return video_path


def delete_file_after_time(file_path, delay):
    """
    Deletes the specified file after a given delay in seconds.
    """
    time.sleep(delay)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path} after {delay} seconds.")
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
