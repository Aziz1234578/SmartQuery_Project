from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('professeur', 'Professeur'),
        ('etudiant', 'Étudiant'),
    )
    OAUTH_PROVIDER_CHOICES = (
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('github', 'GitHub'),
    )

    # Les champs existants de AbstractUser sont déjà : username, first_name, last_name, email, password, etc.
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    oauth_provider = models.CharField(max_length=20, choices=OAUTH_PROVIDER_CHOICES, blank=True, null=True)
    oauth_id = models.CharField(max_length=255, blank=True, null=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
