from django.contrib import admin
from .models import *

# Register your models here.

class ProfesorAdmin(admin.ModelAdmin):
    fields = ['nume', 'prenume', 'specializare']

class MaterieAdmin(admin.ModelAdmin):
    fields = ['titlu', 'durata_ore', 'profesor']

admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Materie, MaterieAdmin)
