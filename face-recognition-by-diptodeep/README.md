# Face Recognition System

## Overview
This project is a face recognition system implemented using OpenCV in Python. The system captures images from a webcam, detects faces using a Haar Cascade classifier, and saves the detected face images to a designated directory. This project can be used for various applications, such as user authentication, attendance systems, and security systems.

## Features
- **Face Detection**: Utilizes Haar Cascade classifier for detecting faces in real-time from webcam input.
- **Image Capture and Storage**: Captures and stores images of detected faces in a specified directory.
- **User Management**: Organizes captured face images in user-specific folders.
- **Video Input Handling**: Processes video input from the default webcam or a specified video source.

## Technology Stack
- **Programming Language**: Python
- **Libraries**: OpenCV, os

## Setup

### Prerequisites
- Python 3.x
- OpenCV library

### Installation
1. **Clone the repository**:
   ```bash
   
   ```
2. **Install dependencies**:
   ```bash
   pip install opencv-python
   ```

3. **Place the Haar Cascade XML file**:
   Ensure the `haarcascade_frontalface_default.xml` file is in the correct directory or update the path in the code to point to its location.

### Running the Application
1. **File run order**:
   ```bash
       python new.py
       python recognize.py
       python check.py
   ```
3. **Follow the prompts**:
   - Enter your name when prompted.
   - The application will capture and save 20 images of your face.

## Usage
- **Starting the application**:
  Run the main script to start the face detection and image capture process. The script will initialize the webcam, detect faces in the video feed, and save the detected faces to the specified directory.
  
- **Captured images**:
  Captured images are stored in the `face_images` directory under subfolders named after the users.


## Contact
For any questions or suggestions, please contact:
- Diptodeep Biswas
- Email: kaininhop@gmail.com

---

## File Descriptions
- `haarcascade_frontalface_default.xml`: Haar Cascade XML file for face detection.
- `new.py`: Script for capturing and saving face images.
- `recognize.py`: Main script to run the face recognition system.
- `checker.py`: it captures the user's face checks if user is recognised or not

Feel free to customize the README as per your project's specifics and add any additional details as required.
