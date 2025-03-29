from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import register, login

urlpatterns = [
    path('admin/', admin.site.urls),

    # Endpoints d'authentification personnalisés
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclusion des URLs d'allauth pour OAuth
    path('accounts/', include('allauth.urls')),
]
