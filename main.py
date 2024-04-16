import requests

import detect
from flask import Flask, jsonify, request
from flask_cors import CORS

# detect.detect("image.jpg")
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "hello world"


@app.route("/detect", methods=["POST"])
def detect_image():
    files = request.files
    file = files.get('file')
    file.save(f"img/{file.filename}")
    # if request.method == "POST":
    #     image = request.files.get('image')
    #
    #     if not image:
    #         return jsonify({"error": "No image provided"}), 400
    #     image.save(f'img/{image.filename}')
    # elif request.method == "GET":
    #     return "detect page"
    fruit_detected = detect.detect(file.filename)
    return jsonify(fruit_detected)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
