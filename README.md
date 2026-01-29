# Face Authentication Attendance System

This project implements a real-time face recognition based attendance system
with punch-in and punch-out functionality using a live camera feed.

## Features
- Face registration
- Face recognition using encodings
- Punch-in / Punch-out attendance
- Real-time camera input
- Basic spoof prevention using live frame checks

## Tech Stack
- Python
- OpenCV
- face_recognition
- NumPy

## How to Run
1. Install dependencies using:
   pip install -r requirements.txt
2. Register face:
   python register_face.py
3. Run attendance system:
   python recognize_face.py

## Limitations
- Low lighting may reduce accuracy
- Covered faces may not be detected
