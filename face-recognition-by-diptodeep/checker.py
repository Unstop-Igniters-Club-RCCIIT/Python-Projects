from pathlib import Path
import face_recognition
import pickle

DEFAULT_OUTPUT_PATH = Path("output")

def encode_known_faces(model: str = "hog") -> None:
    DEFAULT_OUTPUT_PATH.mkdir(exist_ok=True)
    name = input("enter the name ")
    if not Path(f"face_images/{name}").exists():
        print("name not enrolled yet")
        return
    for filepath in Path(f"face_images/{name}").glob("*"):
        print(filepath)
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        if face_encodings:
            # Create a unique filename for each user
            user_filename = DEFAULT_OUTPUT_PATH / f"{name}_encodings.pkl"

            name_encodings = {"names": [name], "encodings": face_encodings}
            with user_filename.open(mode="wb") as f:
                pickle.dump(name_encodings, f)

if __name__ == "__main__":
    encode_known_faces()
