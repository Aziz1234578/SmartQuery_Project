from django.urls import path
from .views import register, login

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    # On pourra ajouter ici d'autres endpoints (ex: callback OAuth, rafraîchissement de token, etc.)
]
