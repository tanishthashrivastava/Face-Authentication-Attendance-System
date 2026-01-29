import cv2
import os

# Ask user name
name = input("Enter your name: ")

# Create folder for user
dataset_path = "dataset"
user_path = os.path.join(dataset_path, name)

if not os.path.exists(user_path):
    os.makedirs(user_path)

# Open camera
cam = cv2.VideoCapture(0)

print("Press 's' to save image, 'q' to quit")

count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        img_path = os.path.join(user_path, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"Image {count} saved")
        count += 1

    elif key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
