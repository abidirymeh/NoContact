<<<<<<< HEAD
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
=======
# NoContact

> Système d'authentification et de contrôle d'ordinateur entièrement sans contact physique : connexion par reconnaissance faciale automatique, navigation par gestes de la main. Développé avec Django, YOLOv8, MediaPipe et face_recognition.

*Projet initié en 1ère année, entièrement repensé, sécurisé et recentré autour d'un vrai concept en 3ème année d'école d'ingénieur.*

## Pourquoi ce projet

Dans les environnements où toucher un clavier/souris pose problème (hygiène en milieu médical, mains occupées, accessibilité pour personnes à mobilité réduite), NoContact propose une alternative : s'authentifier et naviguer sur son ordinateur uniquement avec le visage et les mains — sans un seul clic de souris physique.

Le flux est pensé de bout en bout sans contact :
1. Vous vous asseyez devant l'écran
2. La caméra scanne votre visage automatiquement, en continu, sans bouton à cliquer
3. Une fois reconnu, vous êtes redirigé directement vers le contrôle gestuel — le curseur répond déjà à votre main

## Fonctionnalités

| Fonctionnalité | Statut | Description |
|---|---|---|
| Authentification faciale automatique | ✅ Implémenté | Scan en boucle, sans clic ; connexion dès qu'un visage enregistré est reconnu |
| Souris virtuelle par gestes | ✅ Implémenté | Curseur piloté par l'index (MediaPipe Hands), clic par pincement pouce-index |
| Rappel de posture ergonomique | 🚧 En cours | Alerte en cas de posture prolongée incorrecte (module d'estimation de pose déjà présent côté backend) |
| Lecteur vocal de documents (OCR) | 🚧 Prévu | Lecture à voix haute d'un texte présenté à la caméra, pour l'accessibilité |
| Détection d'objets (YOLOv8) | ⚙️ Module additionnel | Détection en temps réel, présente dans le projet mais indépendante du concept "sans contact" |

## Structure du projet

```
NoContact/
├── facial_auth/            # App Django principale (vision + authentification)
│   ├── detectors/          # Modèles YOLO (yolov4.cfg/.weights — legacy, voir note ci-dessous)
│   ├── migrations/
│   ├── static/              # CSS/JS propres à l'app
│   ├── templates/           # Templates HTML (dashboard, login, souris virtuelle...)
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py          # Backend d'authentification faciale
│   ├── camera_utils.py      # Gestion de la webcam
│   ├── models.py            # UserProfile, FaceProfile
│   ├── urls.py
│   └── views.py
├── myproject/               # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── media/                    # Fichiers médias (non versionné, voir .gitignore)
├── staticfiles/               # Assets statiques collectés
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── yolov8n.pt                # Poids YOLOv8 utilisés par le module de détection d'objets
```

> **Note** : `yolov4.cfg` / `yolov4.weights` référencés dans `settings.py` (`YOLO_CONFIG`) sont des restes d'une ancienne implémentation ; le code actuel (`views.py`) utilise exclusivement `yolov8n.pt` via Ultralytics. À nettoyer avant publication si vous ne les utilisez plus.

## Stack technique

- **Backend** : Django 5.1.7
- **Vision par ordinateur** : OpenCV, face_recognition, MediaPipe
- **Détection d'objets** : YOLOv8 (Ultralytics), PyTorch
- **Base de données** : SQLite (développement)
- **Frontend** : HTML/CSS/JS natif, Bootstrap 5 (pages secondaires), Font Awesome, SweetAlert2

## Prérequis

- Python 3.12
- Webcam
- GPU compatible CUDA (optionnel, accélère YOLO)

## Installation

```bash
git clone https://github.com/abidirymeh/ComputerVision.git
cd ComputerVision

python -m venv myenv
.\myenv\Scripts\activate      # Windows
source myenv/bin/activate     # macOS/Linux

pip install -r requirements.txt
# ou manuellement :
# pip install django==5.1.7 torch ultralytics mediapipe opencv-python face-recognition numpy pillow pyautogui

cp .env.example .env
# Éditez .env avec vos propres valeurs (clé secrète, etc.)

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Accès à l'application : `http://localhost:8000` → redirection automatique vers `/login/`.

> Si l'installation de `face_recognition` échoue, installez `dlib` en premier : `pip install dlib` puis `pip install face-recognition`.

## Sécurité

- Clé secrète et configuration sensibles chargées depuis des variables d'environnement (`.env`), jamais commitées
- `DEBUG=False` par défaut en dehors du développement local
- **Aucune photo n'est stockée** : lors de l'inscription et de la connexion, l'image capturée par la webcam est traitée en mémoire pour en extraire un encodage facial (vecteur de 128 valeurs), puis immédiatement libérée. Seul cet encodage — pas la photo — est conservé en base
- `db.sqlite3` (qui contient les encodages) et l'environnement virtuel (`myenv/`) sont exclus du dépôt via `.gitignore`

## Limites connues

- La détection de vivacité (anti-spoofing) n'est pas encore implémentée : le système ne vérifie pas encore qu'un vrai visage est présent (vs. une photo)
- Reconnaissance faciale non testée en conditions de faible luminosité
- Projet à visée pédagogique — non audité pour un déploiement en production

## Roadmap

- [ ] Détection de vivacité (Eye Aspect Ratio / clignement)
- [ ] Verrouillage automatique par absence de visage
- [ ] Rappel de posture ergonomique
- [ ] Lecteur vocal de documents (OCR + synthèse vocale)
- [ ] Nettoyage des dépendances YOLOv4 obsolètes

## Auteur

**Rimeh Abidi**
Contact : rimeh.abidi@enis.tn

## Licence

MIT — voir `LICENSE.md`
>>>>>>> 726fe35 (NoContact v1.0 : Nettoyage et rebranding)
