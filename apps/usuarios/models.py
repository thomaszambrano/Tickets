# Autor: Thomas Osorio

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    documento = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username