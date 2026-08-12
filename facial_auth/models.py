import cv2
import numpy as np
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import numpy as np
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone


def detect_face(image_path):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    face_encoding = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.username



class FaceProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encoding = models.BinaryField()
    
    image = models.ImageField(
        upload_to='face_images/',
        null=True, 
        blank=True, 
        default='default_face.jpg' 
    )

    def set_encoding(self, face_encoding):
        """Convertit et sauvegarde l'encodage facial"""
        try:
            self.encoding = face_encoding.tobytes()
            self.save()
            return True
        except Exception as e:
            print(f"ERREUR Sauvegarde encodage: {str(e)}")
            return False
    
    def get_encoding(self):
        """Récupère l'encodage facial"""
        try:
            return np.frombuffer(self.encoding, dtype=np.float64)
        except Exception as e:
            print(f"ERREUR Chargement encodage: {str(e)}")
            return None
    @classmethod
    def get_face_profile(cls, face_encoding):
        # Votre logique de recherche
        pass


