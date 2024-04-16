import pathlib
import cv2
import torch
from PIL import Image


def detect(image_path):
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath

    model = torch.hub.load('ultralytics/yolov5', 'custom', path='model/best.pt', force_reload=True)

    # Read image
    image = cv2.imread("img/" + image_path)
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    converted = Image.fromarray(converted)

    results = model(converted, size=640)
    labels = results.names
    for *box, conf, cls in results.xyxy[0]:
        label = f"{labels[int(cls)]}: {conf:.2f}"
        print(label)
        cv2.rectangle(image, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (255, 0, 0), 2)
        cv2.putText(image, label, (int(box[0]), int(box[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imwrite(f'img/{image_path}_detected.jpg', image)
    pathlib.PosixPath = temp
