# face_recognition/forms.py
from django import forms

class FaceUploadForm(forms.Form):
    image = forms.ImageField()
