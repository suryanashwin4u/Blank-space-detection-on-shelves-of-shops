# detect.py

# OpenCV is used for drawing boxes and text on the video frame
import cv2

# YOLO is the object detection model (from Ultralytics)
from ultralytics import YOLO


# ---------------------------------------------------
# LOAD THE TRAINED YOLO MODEL
# ---------------------------------------------------
# best.pt is the model you trained on PRODUCT images
# (not empty shelves directly)
model = YOLO("best.pt")


def detect_blank_space(frame):
    """
    This function:
    1. Detects PRODUCTS using YOLO
    2. Divides the shelf into LEFT, FRONT, RIGHT zones
    3. Decides which zones are EMPTY
    4. Returns:
       - annotated frame (for video)
       - status dictionary (for frontend & audio)
    """

    # Get height (h) and width (w) of the frame
    h, w, _ = frame.shape

    # ---------------------------------------------------
    # STEP 1: DEFINE SHELF ZONES
    # ---------------------------------------------------
    # False means: no product detected yet in that zone
    zones = {
        "left": False,
        "front": False,
        "right": False
    }

    # ---------------------------------------------------
    # STEP 2: RUN YOLO ON THE FRAME
    # ---------------------------------------------------
    # conf=0.4 means YOLO shows detections above 40% confidence
    # device="cpu" keeps laptop safe
    results = model(frame, conf=0.4, device="cpu")

    # ---------------------------------------------------
    # STEP 3: PROCESS EACH DETECTED PRODUCT
    # ---------------------------------------------------
    for r in results:
        for box in r.boxes:

            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Draw a GREEN rectangle around detected product
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),   # Green color
                2
            )

            # Label the box as PRODUCT
            cv2.putText(
                frame,
                "PRODUCT",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # ---------------------------------------------------
            # STEP 4: FIND WHICH ZONE THIS PRODUCT BELONGS TO
            # ---------------------------------------------------
            # Find center x-coordinate of the box
            x_center = (x1 + x2) // 2

            # Divide image width into 3 equal vertical parts
            if x_center < w // 3:
                zones["left"] = True
            elif x_center < 2 * w // 3:
                zones["front"] = True
            else:
                zones["right"] = True

    # ---------------------------------------------------
    # STEP 5: FIND EMPTY ZONES
    # ---------------------------------------------------
    # If a zone has NO product, it is EMPTY
    empty_zones = [
        zone for zone, has_product in zones.items()
        if not has_product
    ]

    # ---------------------------------------------------
    # STEP 6: PREPARE STATUS FOR FRONTEND & AUDIO
    # ---------------------------------------------------
    # Default: shelf is filled
    status = {
        "status": "filled",
        "direction": "",
        "message": "Shelf has products"
    }

    # If at least one empty zone is found
    if empty_zones:
        status = {
            "status": "empty",
            "direction": ", ".join(empty_zones),
            "message": f"Empty shelf detected at {', '.join(empty_zones)}"
        }

        # ---------------------------------------------------
        # STEP 7: DISPLAY EMPTY ZONES ON VIDEO FRAME
        # ---------------------------------------------------
        y_pos = 40  # vertical position for text

        for zone in empty_zones:
            cv2.putText(
                frame,
                f"{zone.upper()} SHELF EMPTY",
                (20, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),  # Red color
                2
            )
            y_pos += 35  # move text downward

    # ---------------------------------------------------
    # STEP 8: RETURN RESULTS
    # ---------------------------------------------------
    return frame, status