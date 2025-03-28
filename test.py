from facial_auth.models import FaceProfile
import face_recognition
import cv2
import numpy as np

# Capturez une nouvelle image pour tester
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(rgb_frame)
    
    if face_locs:
        test_encoding = face_recognition.face_encodings(rgb_frame, face_locs)[0]
        print(f"\nEncodage test (5 premiers): {test_encoding[:5]}")
        
        for profile in FaceProfile.objects.all():
            stored_enc = profile.get_encoding()
            if stored_enc is not None:
                distance = face_recognition.face_distance([stored_enc], test_encoding)
                print(f"Distance avec {profile.user.email}: {distance[0]}")
                if distance[0] < 0.6:
                    print("--> Correspondance trouvée!")
    else:
        print("Aucun visage détecté dans l'image test")
else:
    print("Échec de capture d'image")