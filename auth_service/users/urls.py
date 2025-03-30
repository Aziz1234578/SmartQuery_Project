from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, login, update_role, password_reset_request, password_reset_confirm

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('update-role/', update_role, name='update_role'),
    path('password-reset/', password_reset_request, name='password_reset'),
    path('password-reset-confirm/', password_reset_confirm, name='password_reset_confirm'),
    # Par exemple, pour rafraîchir le token :
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
