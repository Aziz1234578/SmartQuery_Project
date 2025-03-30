from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    register,
    login,
    update_role,
    password_reset_request,
    password_reset_confirm,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/update-role/', update_role, name='update_role'),
    path('auth/password-reset/', password_reset_request, name='password_reset'),
    # URL modifiée pour accepter uidb64 et token
    path('auth/password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('allauth.urls')),
]
