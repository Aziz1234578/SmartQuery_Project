import json
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UtilisateurSerializer

@api_view(['POST'])
def register(request):
    """
    Endpoint d'inscription : crée un nouvel utilisateur.
    """
    serializer = UtilisateurSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    """
    Endpoint de connexion : vérifie les identifiants et retourne des tokens JWT.
    Expects JSON avec "username" et "password".
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # Générer les tokens JWT
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    return Response({'detail': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def update_role(request):
    """
    Permet à l'utilisateur connecté de mettre à jour son rôle.
    Expects JSON: {"role": "etudiant" ou "professeur"}
    """
    role = request.data.get('role')
    if role not in ['etudiant', 'professeur']:
        return Response({"detail": "Rôle invalide."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.role = role
    user.save()
    return Response({"detail": "Rôle mis à jour avec succès."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def password_reset_request(request):
    """
    Demande de réinitialisation du mot de passe.
    Expects JSON: {"email": "adresse@example.com"}
    Envoie un email avec un lien de réinitialisation (contenant uid et token).
    """
    email = request.data.get("email")
    if not email:
        return Response({"detail": "Email requis."}, status=status.HTTP_400_BAD_REQUEST)
    
    form = PasswordResetForm({"email": email})
    if form.is_valid():
        # Générer le contexte pour l'email de réinitialisation
        UserModel = get_user_model()
        associated_users = UserModel.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                # Préparation des données pour l'email
                context = {
                    "email": user.email,
                    "domain": request.get_host(),  # Par ex. 127.0.0.1:8000
                    "site_name": "Smart Query",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "https" if request.is_secure() else "http",
                }
                subject = render_to_string("registration/password_reset_subject.txt", context)
                # Le subject ne doit pas contenir de sauts de ligne
                subject = ''.join(subject.splitlines())
                message = render_to_string("registration/password_reset_email.html", context)
                send_mail(subject, message, None, [user.email])
        # Pour des raisons de sécurité, on retourne toujours le même message
        return Response({"detail": "Si une adresse correspondante existe, un email de réinitialisation a été envoyé."}, status=status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_confirm(request):
    """
    Confirmation de réinitialisation du mot de passe.
    Expects JSON: {"uid": "<uid>", "token": "<token>", "new_password": "nouveauMotDePasse"}
    """
    uidb64 = request.data.get("uid")
    token = request.data.get("token")
    new_password = request.data.get("new_password")
    if not (uidb64 and token and new_password):
        return Response({"detail": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except Exception as e:
        return Response({"detail": "Identifiant invalide."}, status=status.HTTP_400_BAD_REQUEST)
    
    if default_token_generator.check_token(user, token):
        user.set_password(new_password)
        user.save()
        return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Le token n'est pas valide."}, status=status.HTTP_400_BAD_REQUEST)
