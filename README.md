# NoContact

> Système d'authentification et de contrôle d'ordinateur entièrement sans contact physique : connexion par reconnaissance faciale automatique, navigation par gestes de la main. Développé avec Django, YOLOv8, MediaPipe et face_recognition.


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

---
## 📸 Captures d'écran

![image alt](https://github.com/abidirymeh/ComputerVision/blob/fb049591bbada6cde6a4c806b91ff7c7a453947e/inscription.png)
![image alt](https://github.com/abidirymeh/ComputerVision/blob/fb049591bbada6cde6a4c806b91ff7c7a453947e/connexion.png)
![image alt](https://github.com/abidirymeh/ComputerVision/blob/fb049591bbada6cde6a4c806b91ff7c7a453947e/mouse_feed.png)


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


## Auteur

**Rimeh Abidi**
Contact : rimeh.abidi@enis.tn

## Licence

MIT — voir `LICENSE.md`
