import pathlib
import cv2
import torch
from PIL import Image
import pandas as pd
import gunicorn


class Detect:
    def __init__(self):
        # temp = pathlib.PosixPath
        # pathlib.PosixPath = pathlib.WindowsPath
        torch.hub._validate_not_a_forked_repo = lambda a, b, c: True
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=True)
        # pathlib.PosixPath = temp

    def detect_image(self, image_path):
        image = cv2.imread("img/" + image_path)
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

        cv2.imwrite(f'img/{image_path}_detected.jpg', image)
        return fruit_labels_detected
