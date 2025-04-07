from rest_framework import serializers
from .models import Classe, EtudiantsClasse

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'

class EtudiantsClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtudiantsClasse
        fields = '__all__'
