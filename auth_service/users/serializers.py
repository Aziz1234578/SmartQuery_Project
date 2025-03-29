from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'role',
            'oauth_provider',
            'oauth_id',
            'date_inscription'
        ]
        read_only_fields = ['id', 'date_inscription']

    def create(self, validated_data):
        # Crée un utilisateur en hashant son mot de passe
        user = Utilisateur(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
