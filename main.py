from flask import Flask, request, jsonify
import subprocess
import os
import json
import torch
from PIL import Image
import torchvision.transforms as transforms

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def detect():
    image = request.files['image']
    image_path = 'temp.jpg'
    image.save(image_path)

    image = Image.open(image_path)
