import cv2

def simple_face_detection(image_path):
    # Chargez le classificateur Haar pré-entraîné
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces)

print(f"Visages détectés : {simple_face_detection('C:/Users/Anwender/Desktop/i2.png')}")