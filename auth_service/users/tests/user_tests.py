from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Utilisateur

class TestIntegration(APITestCase):  # Le nom commence par "Test"
    def test_full_auth_flow(self):
        # 1. Inscription
        register_url = reverse('register')
        register_data = {
            "username": "integrationuser",
            "first_name": "Integration",
            "last_name": "Test",
            "email": "integration@example.com",
            "password": "integrate123",
            "role": "etudiant"
        }
        register_response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        # 2. Connexion
        login_url = reverse('login')
        login_data = {
            "username": "integrationuser",
            "password": "integrate123"
        }
        login_response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', login_response.data)
        refresh_token = login_response.data['refresh']

        # 3. Rafraîchissement du token
        refresh_url = reverse('token_refresh')
        refresh_data = {"refresh": refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
