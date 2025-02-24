from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profesori', views.afisareProfesori, name='afisareProfesori'),
    path('materii/<str:code>', views.afisareMaterii, name='afisareMaterii'),
    path('adauga_materie', views.adaugaMaterie, name='adaugaMaterie'),

]
