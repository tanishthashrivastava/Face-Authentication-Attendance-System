import face_recognition
import cv2
import os
import csv
from datetime import datetime
import numpy as np

# Paths
DATASET_PATH = "dataset"
ATTENDANCE_FILE = "attendance.csv"

# Load known faces
known_face_encodings = []
known_face_names = []

print("Loading registered faces...")

for person_name in os.listdir(DATASET_PATH):
    person_folder = os.path.join(DATASET_PATH, person_name)

    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_face_encodings.append(encodings[0])
            known_face_names.append(person_name)

print("Faces loaded successfully")

# Open camera
video_capture = cv2.VideoCapture(0)

# Fix camera resolution (professional touch)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

marked_today = {}
today_date = datetime.now().strftime("%Y-%m-%d")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        name = "Unknown"

        if len(known_face_encodings) > 0:
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)

            # Threshold for better accuracy
            if face_distances[best_match_index] < 0.5:
                name = known_face_names[best_match_index]

        # Ignore unknown faces (professional behaviour)
        if name == "Unknown":
            continue

        current_time = datetime.now().strftime("%H:%M:%S")

        # Punch-In
        if name not in marked_today:
            marked_today[name] = today_date + "_IN"

            with open(ATTENDANCE_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, today_date, current_time, ""])

            print(f"{name} Punch-In at {current_time}")

        # Punch-Out
        elif marked_today[name] == today_date + "_IN":
            marked_today[name] = today_date + "_OUT"

            rows = []
            with open(ATTENDANCE_FILE, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)

            for row in rows[::-1]:
                if row[0] == name and row[3] == "":
                    row[3] = current_time
                    break

            with open(ATTENDANCE_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            print(f"{name} Punch-Out at {current_time}")

        # Draw box and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(
            frame,
            name,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2,
        )

    cv2.imshow("Face Authentication Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
print("Attendance system closed safely.")
