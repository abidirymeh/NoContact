MyProject: VisionLibrary



**Project Overview**

MyProject is a sophisticated Django-based web application that integrates advanced computer vision and facial authentication capabilities. Leveraging state-of-the-art libraries such as YOLOv8, MediaPipe, and face_recognition, it provides a secure and interactive platform for real-time vision AI applications. Key features include facial recognition for user authentication, object detection, hand gesture-based virtual mouse control, and extensible modules for pose estimation, OCR, and style transfer.

**Key Features**

Facial Authentication: Secure user registration and login using facial recognition.
Object Detection: Real-time object detection powered by YOLOv4 and YOLOv8 models.
Virtual Mouse Control: Intuitive mouse navigation using hand gestures via MediaPipe.
Pose Estimation: Body keypoint detection for posture analysis (in development).
OCR & Style Transfer: Planned features for text recognition and artistic image processing.

**Project Structure**

MYPROJECT/
├── ComputerVision/         # Computer vision utilities
├── Debug_images/           # Debug image outputs
├── Facial_auth/            # Core Django app for vision and authentication
│   ├── detectors/          # YOLO model files (yolov4.cfg, yolov4.weights, coco.names)
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates for user interface
│   ├── admin.py            # Admin panel configuration
│   ├── apps.py             # Application configuration
│   ├── backends.py         # Custom facial authentication backend
│   ├── camera_utils.py     # Webcam management utilities
│   ├── models.py           # Database models (UserProfile, FaceProfile)
│   ├── urls.py             # URL routing
│   ├── views.py            # Request handling and logic
├── Media/                  # User-uploaded media (e.g., face images)
├── Myenv/                  # Virtual environment
├── Myproject/              # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Project-level URL routing
│   ├── asgi.py             # ASGI configuration
│   ├── wsgi.py             # WSGI configuration
├── Staticfiles/            # Collected static assets
├── .gitattributes          # Git attributes
├── .gitignore              # Git ignore configuration
├── db.sqlite3              # SQLite database
├── face_recognition.log    # Facial recognition logs
├── logging_config.py       # Logging configuration
├── manage.py               # Django management script
├── yolov8n.pt              # YOLOv8 model weights

**Getting Started**

Follow these steps to set up and run the project locally.
Prerequisites
Python 3.12: Ensure Python 3.12 is installed.
Virtual Environment: Recommended for isolated dependency management.
Webcam: Required for facial authentication and virtual mouse features.
Optional GPU: CUDA-enabled GPU for accelerated YOLO processing.

**Dependencies:**
Django 5.1.7
PyTorch
Ultralytics (YOLO)
MediaPipe
OpenCV-Python
face_recognition
NumPy
Pillow
PyAutoGUI
optree (>=0.13.0)


Installation
**Clone the Repository:**
git clone https://github.com/abidirymeh/ComputerVision.git
cd MYPROJECT

**Set Up Virtual Environment:**
python -m venv myenv
.\myenv\Scripts\activate  # Windows
source myenv/bin/activate  # macOS/Linux

**Install Dependencies:**

pip install django==5.1.7 torch ultralytics mediapipe opencv-python face-recognition numpy pillow pyautogui
pip install --upgrade 'optree>=0.13.0'

For GPU support, install the appropriate CUDA-enabled PyTorch version from the PyTorch official website.

Note: If face_recognition installation fails, install dlib first:

pip install dlib
pip install face-recognition

**Download YOLO Model Files:**
Place the following files in facial_auth/detectors/:
yolov4.cfg: Download
yolov4.weights: Download
coco.names: Download
Ensure yolov8n.pt is present in the project root.

**Apply Database Migrations:**

python manage.py makemigrations
python manage.py migrate

**Starting the Application**

Launch the Django development server:

python manage.py runserver

Access the application at http://localhost:8000.

Expected Outcome:
The application redirects to /login/ for facial authentication.
Upon successful login, the dashboard provides access to features like object detection, virtual mouse control, and facial analysis.

**Built With**
Django 5.1.7: Web framework for rapid development and security.
PyTorch & Ultralytics: YOLOv8 for high-performance object detection.
MediaPipe: Real-time hand tracking for virtual mouse control.
face_recognition: Robust facial recognition for authentication.
OpenCV-Python: Advanced image processing.
Bootstrap 5: Responsive front-end framework.
Font Awesome: Iconography for enhanced UI.
SweetAlert2: Elegant user notifications.
Visual Studio Code: Development environment.

**Contributing**

We welcome contributions to enhance MyProject. Please review the CONTRIBUTING.md file (create one if absent) for guidelines on submitting issues, feature requests, or pull requests.

**Versioning**
Latest Stable Version: 1.0
Current Version: 1.0


**Authors**
Rimeh ABIDI


**License**
This project is licensed under the MIT License. See the LICENSE.md file for details.

**Troubleshooting**
ModuleNotFoundError: No module named 'mediapipe':
Verify the virtual environment is activated: .\myenv\Scripts\activate.
Check installation: pip show mediapipe.



Install: pip install mediapipe.
Ensure compatibility with Python 3.12 and resolve any environment mismatches.



Webcam Connectivity Issues:
Confirm webcam permissions are granted.
Verify cv2.CAP_DSHOW or cv2.CAP_MSMF backend support in camera_utils.py.

YOLO Model Errors:
Ensure yolov4.cfg, yolov4.weights, coco.names, and yolov8n.pt are correctly placed.
For GPU acceleration, install CUDA and cuDNN compatible with your PyTorch version.

face_recognition Installation:
If errors occur, install dlib dependency first:

pip install dlib
pip install face-recognition

Contact

For inquiries or support, contact the project maintainer at rimeh.abidi@enis.tn.
