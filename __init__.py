import base64
import requests
from detect import Detect
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import gevent


def create_app():
    app = Flask(__name__)
    CORS(app)
    detect_model = Detect()

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route("/detect", methods=["POST"])
    def detect_image():
        files = request.files
        file = files.get('file')
        file.save(f"img/{file.filename}")
        fruit_detected = detect_model.detect_image(file.filename)
        image_path = f'img/{file.filename}_detected.jpg'
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        fruit_detected['image'] = img_data

        return jsonify(fruit_detected)

    return app

# if __name__ == '__main__':
#     detect_model = Detect()
#     app.run(host='0.0.0.0', debug=True)
