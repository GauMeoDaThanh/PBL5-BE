import base64
import requests
from detect import Detect
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/detect", methods=["POST"])
def detect_image():
    file = request.files['image']
    fruit_detected = detect_model.detect_image(file)

    return jsonify(fruit_detected)


if __name__ == '__main__':
    detect_model = Detect()
    app.run(host='0.0.0.0', debug=True)
