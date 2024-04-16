from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from enum import Enum



# Definirajte moguće vrijednosti za korisničke uloge
USER_ROLES = (
    ('student', 'Student'),
    ('admin', 'Admin'),
    ('profesor', 'Profesor'),
)

# Definicija proširenog korisničkog modela sa atributom za ulogu korisnika
class CustomUser(AbstractUser):
  
    # Polje role s ograničenim mogućim vrijednostima
      role = models.CharField(max_length=10, choices=USER_ROLES)
      

class Dokument(models.Model):
    naslov = models.CharField(max_length=100)
    putanja = models.CharField(max_length=200)
    vrijeme_kreiranja = models.DateTimeField(auto_now_add=True)
    kreator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class StudentDokument(models.Model):
    dokument = models.ForeignKey(Dokument, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)