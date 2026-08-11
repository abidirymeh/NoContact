import cv2
import time

class CameraManager:
    def __init__(self):
        self.cap = None
        self.last_error_time = 0
        
    def get_camera(self):
        """Obtient une instance de caméra avec reconnexion automatique"""
        if self.cap and self.cap.isOpened():
            return self.cap
            
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if self.cap.isOpened():
                self._configure_camera()
                return self.cap
        except:
            pass
            
        return None
        
    def _configure_camera(self):
        """Configure les paramètres de la caméra"""
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
    def release(self):
        if self.cap:
            self.cap.release()
            self.cap = None