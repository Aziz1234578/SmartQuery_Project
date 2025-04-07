from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Les routes de l’app "classes"
    path('', include('classes.urls')),
]
