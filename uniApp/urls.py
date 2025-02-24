from django.urls import path, re_path
from . import views
urlpatterns = [
	path("", views.index, name="index"),
    path("mesaj", views.mesaj, name="mesaj"),
    path("data", views.data, name="data"),
    path("nr_accesari", views.nr_accesari, name="nr_accesari"),
    path("suma", views.suma, name="suma"),
    path("text", views.text, name="text"),
    path("nr_parametri", views.nr_parametri, name="nr_parametri"),
    path("operatie", views.operatie, name="operatie"),
    path("tabel", views.tabel, name="tabel"),
    path('lista', views.lista, name='lista'),
    path("adunare_numere/<str:userInput>", views.adunare_numere, name='adunare_numere'),
    path('afisare_liste', views.afisare_liste, name='afisare_liste'),
    path('nume_corect/<str:nume>', views.numara_nume, name='numara_nume'),
    path('subsir/<str:userInput>', views.cauta_subsir, name='cauta_subsir')

    # re_path(r"^suma.*$", views.suma, name="suma"),
]

