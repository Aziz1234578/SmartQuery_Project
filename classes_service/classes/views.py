from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Classe, EtudiantsClasse
from .serializers import ClasseSerializer, EtudiantsClasseSerializer

# Exemple basique: on imagine qu'on a un JWT contenant user.id et potentiellement user.role
# Pour un vrai usage, on ferait un appel HTTP au service Auth ou on lirait le token plus finement.

class ClasseCreateView(generics.CreateAPIView):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Dans la réalité, on vérifierait le rôle = professeur
        # Ex: if self.request.user.role != 'professeur': ...
        # Ici, on suppose que request.user.id = le professeur
        serializer.save(professeur_id=self.request.user.id)

class ClasseListView(generics.ListAPIView):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]

class ClasseUpdateView(generics.UpdateAPIView):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    # On pourrait override pour vérifier que request.user.id == professeur_id

class InscrireEtudiantView(generics.CreateAPIView):
    queryset = EtudiantsClasse.objects.all()
    serializer_class = EtudiantsClasseSerializer
    permission_classes = [IsAuthenticated]

class DesinscrireEtudiantView(generics.DestroyAPIView):
    queryset = EtudiantsClasse.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # ID = enregistrement d’EtudiantsClasse
