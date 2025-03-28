from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import facial_auth
import json
import numpy as np
from .models import UserProfile

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import FaceProfile
User = get_user_model()

class FaceAuthBackend(ModelBackend):
    def authenticate(self, request, face_encoding=None):
        # Votre logique d'authentification faciale
        try:
            profile = FaceProfile.objects.get_face_profile(face_encoding)
            return profile.user
        except FaceProfile.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None