# app.py
from flask import Flask, render_template, Response
import cv2
from detect import detect_blank_space

app = Flask(__name__)

def generate_frames():
    import time
    import cv2

    camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    time.sleep(1)

    if not camera.isOpened():
        print("CAMERA NOT OPENED")
        return

    print("CAMERA OPENED")

    while True:
        success, frame = camera.read()
        if not success:
            print("FRAME READ FAILED")
            break

        frame = detect_blank_space(frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            print("JPEG ENCODE FAILED")
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            buffer.tobytes() +
            b"\r\n"
        )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        threaded=True,
        use_reloader=False
    )

