# Blank Space Detection on Shelves (Web App)

## Project Overview

This project is a computer vision–based web application that detects blank or empty spaces on shop shelves using YOLO (You Only Look Once) object detection.
It is designed as a working demo project for academic events such as Synergy at SGT University and for learning AI and web integration.

The system processes live webcam or video input and highlights shelf areas where products are missing.

---

## Objectives

* Detect empty spaces on retail shelves
* Use real-time object detection
* Provide a simple web-based interface
* Demonstrate practical AI application for retail analytics

---

## Tech Stack

* Python
* Flask (Web Framework)
* YOLOv8 (Ultralytics)
* OpenCV
* HTML, CSS, JavaScript

---

## Project Structure

```
blank_space_detection_web_app/
│
├── app.py                 # Main Flask application
├── detect.py              # Detection logic
├── yolov8n.pt             # YOLO model
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
│
├── model/                 # Model related files
├── utils/                 # Helper functions
├── static/                # CSS, JS, images
├── templates/             # HTML templates
```

---

## How to Run the Project Locally

### Step 1: Clone the repository

```bash
git clone https://github.com/USERNAME/blank_space_detection_web_app.git
cd blank_space_detection_web_app
```

---

### Step 2: Create virtual environment

```bash
python -m venv venv
```

---

### Step 3: Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

---

### Step 4: Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 5: Run the application

```bash
python app.py
```

---

### Step 6: Open in browser

```
http://127.0.0.1:5000
```

---

## Collaboration Guidelines

* Do not push `venv/` or `__pycache__/`
* Update `requirements.txt` when adding new libraries
* Use clear and meaningful commit messages
* Follow the existing project folder structure

---

## Use Case

* Retail shelf monitoring
* Inventory gap detection
* Smart store analytics
* Academic demonstrations and research

---

## Future Enhancements

* Accuracy improvement with a custom-trained model
* Product count and analytics
* Cloud deployment
* Dashboard for store managers

---

## Author

Ashwani Kumar
Assistant Professor, Computer Applications
SGT University

---

## License

This project is intended for educational and research purposes only.
