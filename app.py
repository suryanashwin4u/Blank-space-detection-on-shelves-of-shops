# app.py

from flask import Flask, render_template, Response, jsonify
import cv2
import time
import pyttsx3
from detect import detect_blank_space

app = Flask(__name__)

# ---------- Text to Speech ----------
engine = pyttsx3.init()
engine.setProperty("rate", 150)

last_spoken = None
latest_status = {
    "status": "detecting",
    "direction": "",
    "message": "Detection started"
}

def speak(message):
    global last_spoken
    if message and message != last_spoken:
        engine.say(message)
        engine.runAndWait()
        last_spoken = message

# ---------- Camera Stream ----------
def generate_frames():
    global latest_status

    camera = cv2.VideoCapture(0)
    time.sleep(1)

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame, status_data = detect_blank_space(frame)

        # update status for frontend
        latest_status = status_data

        # speak for visually impaired
        speak(status_data["message"])

        ret, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame_bytes +
            b"\r\n"
        )

# ---------- Routes ----------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/status")
def status():
    return jsonify(latest_status)

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
