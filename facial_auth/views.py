from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
import face_recognition
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import json  # Ajout pour json.loads
from .models import FaceProfile  # Import de votre modèle
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
def face_registration(request):
    if request.method == 'POST':
        try:
            # 1. Récupérer les données
            email = request.POST.get('email')
            password = request.POST.get('password')
            image_data = request.POST.get('face_image')
            
            if not all([email, password, image_data]):
                return JsonResponse({'error': 'Tous les champs sont requis'}, status=400)
            
            # 2. Convertir l'image
            img_str = image_data.split(',')[1]
            img_bytes = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_bytes))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # 3. Encodage facial
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_frame)
            
            if not encodings:
                return JsonResponse({'error': 'Aucun visage détecté'}, status=400)
            
            # 4. Vérifier si l'utilisateur existe déjà
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Cet email est déjà utilisé'}, status=400)
            
            # 5. Créer l'utilisateur et le profil
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            
            FaceProfile.objects.create(
                user=user,
                encoding=encodings[0].tobytes()
            )
            
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

def face_login(request):
    if request.method == 'POST':
        try:
            # 1. Récupérer l'image
            data = json.loads(request.body)
            image_data = data.get('face_image')
            
            if not image_data:
                return JsonResponse({'error': 'Aucune image reçue'}, status=400)
            
            # 2. Convertir l'image
            img_str = image_data.split(',')[1]
            img_bytes = base64.b64decode(img_str)
            img = Image.open(BytesIO(img_bytes))
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # 3. Comparaison faciale
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if not face_locations:
                return JsonResponse({'error': 'Aucun visage détecté'}, status=400)
                
            current_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            
            # 4. Recherche dans la base
            for profile in FaceProfile.objects.select_related('user').all():
                stored_encoding = np.frombuffer(profile.encoding, dtype=np.float64)
                matches = face_recognition.compare_faces(
                    [stored_encoding],
                    current_encoding,
                    tolerance=0.6  # Seuil de tolérance
                )
                
                if matches[0]:
                    user = profile.user
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, profile.user)
                    return JsonResponse({
                        'status': 'success',
                        'redirect': '/dashboard/'
                    })
            
            return JsonResponse({
                'status': 'error',
                'message': 'Visage non reconnu'
            }, status=401)
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erreur technique: {str(e)}'
            }, status=500)
    
    return render(request, 'face_auth/face_login.html')
@login_required
def dashboard(request):
    """Vue protégée accessible seulement après authentification"""
    return render(request, 'face_auth/dashboard.html')


@login_required
def custom_logout(request):
    logout(request)
    return redirect('facial_auth:login')