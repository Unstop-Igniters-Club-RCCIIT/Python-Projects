import cv2
import os
def start ():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(1)

    output_folder = 'face_images'
    os.makedirs(output_folder, exist_ok=True)

    user_name = input("Enter your name: ")

    user_folder = os.path.join(output_folder, user_name)
    os.makedirs(user_folder, exist_ok=True)

    photo_count = 0
    no_face_count = 0
    max_no_face_count = 10

    while photo_count < 20:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=6)

        if len(faces) > 0:
            no_face_count = 0
            x, y, w, h = faces[0]
            face = frame[y:y + h, x:x + w]
            photo_count += 1
            filename = os.path.join(user_folder, f'{user_name}_{photo_count}.jpg')
            cv2.imwrite(filename, face)
            print(f"Face {photo_count} saved as {filename}")
        else:
            print("Face not found")
            no_face_count += 1
            if no_face_count >= max_no_face_count:
                print(f"No face found for {max_no_face_count} consecutive frames. Closing the webcam.")
                os.removedirs(user_folder)
                break
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    start()
