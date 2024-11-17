import os
from pathlib import Path
import face_recognition
import pickle
from collections import Counter
import cv2
def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def recognize_faces(
    image_location: str,
    encodings_location: Path,
    model: str = "hog",
) -> None:
    print(f"Opening encodings file: {encodings_location}")
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(
        input_image, model=model
    )
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )
    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        print(name, bounding_box)
if os.path.exists("unknown.jpg"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face = frame[y:y + h, x:x + w]
        filename = 'unknown.jpg'
        cv2.imwrite(filename, face)
        cap.release()
    else:
        print("No faces detected.")
        exit
x = input("Enter your name: ")
encodings_location = Path("output") / f"{x}_encodings.pkl"
recognize_faces("unknown.jpg", encodings_location)
