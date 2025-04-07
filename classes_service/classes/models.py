from django.db import models
from django.utils import timezone

class Classe(models.Model):
    nom_classe = models.CharField(max_length=255)
    professeur_id = models.IntegerField()  # ID d'un user (rôle=prof) du service Auth
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom_classe

class EtudiantsClasse(models.Model):
    etudiant_id = models.IntegerField()  # ID d'un user (rôle=etudiant) du service Auth
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='etudiants')

    class Meta:
        unique_together = ('etudiant_id', 'classe')

    def __str__(self):
        return f'Etudiant {self.etudiant_id} dans {self.classe.nom_classe}'
