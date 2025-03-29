from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'date_inscription')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'oauth_provider', 'oauth_id')}),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
