import cv2
import os
from deepface import DeepFace

def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle on each face
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    output_path = os.path.join("static", "uploads", "detected_" + os.path.basename(image_path))
    cv2.imwrite(output_path, img)
    return output_path, len(faces)

def recognize_face(upload_path, known_folder="known_faces"):
    matches = []
    for known_img in os.listdir(known_folder):
        known_path = os.path.join(known_folder, known_img)
        try:
            result = DeepFace.verify(upload_path, known_path, enforce_detection=False)
            if result["verified"]:
                matches.append({
                    "name": os.path.splitext(known_img)[0],
                    "distance": round(result["distance"], 3)
                })
        except:
            continue
    return matches
