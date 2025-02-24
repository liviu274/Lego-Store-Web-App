from django.db import models

# Create your models here.
class TestModel(models.Model):
    nr = models.DecimalField(max_digits=5, decimal_places=2)

class Profesor(models.Model):
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    specializare = models.CharField(max_length=50)

class Materie(models.Model):
    titlu = models.CharField(max_length=50)
    durata_ore = models.IntegerField(default=5)

    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, null=True)