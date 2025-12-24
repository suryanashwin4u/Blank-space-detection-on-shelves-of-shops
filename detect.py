# detect.py
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model (pretrained)
model = YOLO("yolov8n.pt")  # lightweight & fast

def detect_blank_space(frame):
    """
    Detect products and highlight blank spaces
    """
    h, w, _ = frame.shape

    # Run YOLO detection
    results = model(frame, conf=0.4, device="cpu")

    product_boxes = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            # COCO classes: bottle, box, etc (products)
            if cls in [39, 40, 41, 44]:  # bottle, cup, bowl (approx products)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                product_boxes.append((x1, y1, x2, y2))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # If few products → assume blank space
    if len(product_boxes) < 2:
        cv2.putText(
            frame,
            "BLANK SPACE DETECTED",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )
        cv2.rectangle(frame, (10, 10), (w - 10, h - 10), (0, 0, 255), 4)

    return frame
