import pathlib
import cv2
import torch
from PIL import Image
import base64
import numpy as np
from io import BytesIO


class Detect:
    def __init__(self):
        temp = pathlib.PosixPath
        pathlib.PosixPath = pathlib.WindowsPath
        torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=True)
        pathlib.PosixPath = temp

    def detect_image(self, image):
        image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)
        converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        converted = Image.fromarray(converted)

        results = self.model(converted, size=640)
        labels = results.names
        fruit_labels_detected = {"fruits": {}}
        for *box, conf, cls in results.xyxy[0]:
            label = f"{labels[int(cls)]}: {conf:.2f}"
            cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
            cv2.putText(image, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
            # Count the number of fruit detected
            fruit_labels_detected["fruits"][labels[int(cls)]] = fruit_labels_detected["fruits"].get(labels[int(cls)],
                                                                                                    0) + 1

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image)
        byte_arr = BytesIO()
        pil_img.save(byte_arr, format='JPEG')
        encoded_image = base64.b64encode(byte_arr.getvalue()).decode('utf-8')

        fruit_labels_detected["image"] = encoded_image
        return fruit_labels_detected
