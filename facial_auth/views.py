import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
os.environ['OPENCV_VIDEOIO_PRIORITY_DSHOW'] = '1'

import cv2
import numpy as np
import face_recognition
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import FaceProfile
from PIL import Image
from io import BytesIO
import base64
import json
import time
import torch
from ultralytics import YOLO

cv2.setNumThreads(1)

try:
    yolo_model = YOLO('yolov8n.pt')
    if torch.cuda.is_available():
        yolo_model.to('cuda')
except Exception as e:
    print(f"Erreur chargement YOLO: {e}")
    yolo_model = None

def detect_objects(frame):
    if yolo_model:
        results = yolo_model(frame)
        return results[0].plot()
    return frame

def detect_hands(frame):
    if yolo_model:
        results = yolo_model(frame, classes=[0])
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return frame

def get_video_capture():
    """Version finale avec gestion d'erreur renforcée"""
    backends = [cv2.CAP_DSHOW, 0]  
    
    for index in [0, 1]:
        for backend in backends:
            try:
                cap = cv2.VideoCapture(index, backend)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS, 30)
                    print(f"Webcam connectée (index:{index}, backend:{backend})")
                    return cap
            except:
                continue
    print("Aucune webcam accessible")
    return None



def preprocess_frame(frame):
    gamma = 1.8
    table = np.array([((i / 255.0) ** (1.0 / gamma)) * 255 for i in np.arange(256)]).astype("uint8")
    frame = cv2.LUT(frame, table)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = clahe.apply(l)
    frame = cv2.merge((l, a, b))
    frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)
    return frame


def generate_frames():
    cap = None
    try:
        while True:
            try:
                if cap is None or not cap.isOpened():
                    cap = get_video_capture()
                    if cap is None:
                        time.sleep(2)
                        continue

                success, frame = cap.read()
                if not success:
                    cap.release()
                    cap = None
                    time.sleep(1)
                    continue

                frame = detect_objects(frame)
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                yield (b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + 
                      buffer.tobytes() + b'\r\n')

            except Exception as e:
                print(f"Erreur vidéo: {e}")
                if cap:
                    cap.release()
                    cap = None
                time.sleep(1)
    finally:
        if cap is not None:
            cap.release()
            print("Caméra relâchée (fin du flux détection d'objets)")




@csrf_exempt
def face_registration(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            image_data = request.POST.get('face_image')
            
            if not all([email, password, image_data]):
                return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)
            
            try:
                img_str = image_data.split(',')[1]
                img_bytes = base64.b64decode(img_str)
                img = Image.open(BytesIO(img_bytes))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                return JsonResponse({'error': f'Erreur de traitement d\'image: {str(e)}'}, status=400)
            
            try:
                encodings = face_recognition.face_encodings(rgb_frame)
                if not encodings:
                    return JsonResponse({'error': 'Aucun visage détecté'}, status=400)
            except Exception as e:
                return JsonResponse({'error': f'Erreur de reconnaissance faciale: {str(e)}'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Cet email est déjà utilisé'}, status=400)
            
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )
                
                FaceProfile.objects.create(
                    user=user,
                    encoding=encodings[0].tobytes()
                )
            except Exception as e:
                return JsonResponse({'error': f'Erreur de création de compte: {str(e)}'}, status=500)
            
            return JsonResponse({
                'status': 'success',
                'redirect': '/login/'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return render(request, 'face_auth/face_registration.html')

@csrf_exempt
def face_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('face_image')
            
            if not image_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Aucune image fournie',
                    'person': 'undefined'
                }, status=400)
            
            try:
                img_str = image_data.split(',')[1]
                img_bytes = base64.b64decode(img_str)
                img = Image.open(BytesIO(img_bytes))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Erreur de traitement d\'image: {str(e)}',
                    'person': 'undefined'
                }, status=400)
            
            try:
                face_locations = face_recognition.face_locations(rgb_frame)
                if not face_locations:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Aucun visage détecté',
                        'person': 'undefined'
                    }, status=400)
                
                current_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Erreur de détection faciale: {str(e)}',
                    'person': 'undefined'
                }, status=400)
            
            try:
                for profile in FaceProfile.objects.select_related('user').all():
                    stored_encoding = np.frombuffer(profile.encoding, dtype=np.float64)
                    matches = face_recognition.compare_faces(
                        [stored_encoding], 
                        current_encoding,
                        tolerance=0.6
                    )
                    
                    if matches[0]:
                        user = profile.user
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Reconnaissance réussie',
                            'person': profile.user.username,
                            'redirect': '/mouse/'
                        })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Erreur de comparaison: {str(e)}',
                    'person': 'undefined'
                }, status=500)
            
            return JsonResponse({
                'status': 'error',
                'message': 'Visage non reconnu',
                'person': 'undefined'
            }, status=401)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'person': 'undefined'
            }, status=500)
    
    return render(request, 'face_auth/face_login.html')

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'face_auth/dashboard.html')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('facial_auth:login')








@csrf_exempt
def video_feed(request):
    try:
        return StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@csrf_exempt
def object_detection(request):
    if request.method == 'GET':
        return render(request, 'face_auth/object_detection.html')
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def pose_estimation(request):
    if request.method == 'POST':
        try:
            image_data = request.POST.get('image', '').split(',')[1]
            img_bytes = base64.b64decode(image_data)
            img_np = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            
            if yolo_model:
                results = yolo_model(img)
                annotated_image = results[0].plot()
            else:
                annotated_image = img

            _, buffer = cv2.imencode('.jpg', annotated_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return JsonResponse({
                'status': 'success',
                'processed_image': f"data:image/jpeg;base64,{img_base64}"
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)








@csrf_exempt
def activate_camera(request):
    if request.method == 'POST':
        try:
            # Votre logique d'activation ici
            print("Activation de la caméra")  # Vérifiez dans la console serveur
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=400)



@csrf_exempt
def pose_estimation(request):
    if request.method == 'POST':
        try:
            image_data = request.POST.get('image', '').split(',')[1]
            img_bytes = base64.b64decode(image_data)
            img_np = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
            
            if yolo_model:
                results = yolo_model(img)
                annotated_image = results[0].plot()
            else:
                annotated_image = img

            _, buffer = cv2.imencode('.jpg', annotated_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return JsonResponse({
                'status': 'success',
                'processed_image': f"data:image/jpeg;base64,{img_base64}"
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)






import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialisation MediaPipe
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)




def mouse_feed(request):
    return render(request, 'face_auth/mouse_feed.html')

def generate_mouse_frames():
    cap = get_video_capture()
    if cap is None:
        return
    screen_width, screen_height = pyautogui.size()

    # Variables pour le contrôle de la souris
    prev_x, prev_y = 0, 0
    hand_detected = False
    click_threshold = 0.05
    frame_count = 0

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands_detector.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Dessiner les landmarks de la main
                    mp.solutions.drawing_utils.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    # Récupérer les coordonnées du bout de l'index
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    # Convertir les coordonnées normalisées en coordonnées d'écran
                    h, w, _ = frame.shape
                    x = int(index_tip.x * w)
                    y = int(index_tip.y * h)

                    # Contrôle de la souris (toutes les 2 frames pour fluidité)
                    if frame_count % 2 == 0:
                        screen_x = np.interp(index_tip.x, [0.1, 0.9], [0, screen_width])
                        screen_y = np.interp(index_tip.y, [0.1, 0.9], [0, screen_height])
                        pyautogui.moveTo(screen_x, screen_y)

                        # Détection de clic (pouce et index proches)
                        distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
                        if distance < click_threshold:
                            pyautogui.click()
                            cv2.circle(frame, (x, y), 20, (0, 255, 0), -1)

                    # Dessiner un cercle sur le bout de l'index
                    cv2.circle(frame, (x, y), 10, (255, 0, 0), -1)

                    hand_detected = True
            else:
                hand_detected = False

            frame_count += 1
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        # Toujours relâcher la caméra, même si le client se déconnecte
        # (navigation, déconnexion) ou qu'une exception survient.
        if cap is not None:
            cap.release()
            print("Caméra relâchée (fin du flux souris)")

def mouse_video_feed(request):
    return StreamingHttpResponse(
        generate_mouse_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )