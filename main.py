import requests

import detect
from flask import Flask, jsonify, request

# detect.detect("image.jpg")
app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route("/detect")
def detect_image():
    if request.method == "POST":
        image = request.files.get('image')

        if not image:
            return jsonify({"error": "No image provided"}), 400
        image.save(f'img/{image.filename}')
    elif request.method == "GET":
        return "detect page"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
