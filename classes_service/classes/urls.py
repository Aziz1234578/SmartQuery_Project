from django.urls import path
from .views import (
    ClasseCreateView,
    ClasseListView,
    ClasseUpdateView,
    InscrireEtudiantView,
    DesinscrireEtudiantView,
)

urlpatterns = [
    path('classes/', ClasseListView.as_view(), name='classes_list'),
    path('classes/create/', ClasseCreateView.as_view(), name='classes_create'),
    path('classes/<int:id>/update/', ClasseUpdateView.as_view(), name='classes_update'),
    path('classes/inscrire/', InscrireEtudiantView.as_view(), name='inscrire_etudiant'),
    path('classes/desinscrire/<int:id>/', DesinscrireEtudiantView.as_view(), name='desinscrire_etudiant'),
]
