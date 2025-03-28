from django.contrib import admin
from .models import UserProfile  # L'import relatif avec le point

# Le reste de votre configuration admin...
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'face_encoding_exists')
    
    def face_encoding_exists(self, obj):
        return bool(obj.face_encoding)
    face_encoding_exists.boolean = True