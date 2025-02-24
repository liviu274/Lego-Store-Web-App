from django.shortcuts import render
from datetime import datetime
from uniApp import models
import re
import typing

# Create your views here.

ACCESS_COUNT = 0
MYSUMA = 0
VALID_ACCESS_COUNT = 0

from django.http import HttpResponse

def index(request):
    return HttpResponse('Primul raspuns')

def mesaj(request):
    return HttpResponse('Mesaj')

def data(request):
    now = datetime.now()
    myCurrentDate = now.strftime("%d/%m/%y")
    return HttpResponse(now)

def nr_accesari(request):
    global ACCESS_COUNT
    ACCESS_COUNT += 1
    return HttpResponse(ACCESS_COUNT)

def suma(request):
    a = int(request.GET.get("a", 0))
    b = int(request.GET.get("b", 0))
    s = a+b
    return HttpResponse(f"Suma dintre {a} si {b} este: {s}")

def text(request):
    t = str(request.GET.get("t", 0))
    isOnlyAlpha = True
    for char in t:
        if char.isalpha() == False:
            isOnlyAlpha = False
            break    
    if isOnlyAlpha == True:
        return HttpResponse(f"textul urmator contine doar caractere: {t}")
    else:
        return HttpResponse("textul nu contine doar caractere")
    
def nr_parametri(request):
    parametri = request.GET
    nr_parametri = len(parametri)
    return HttpResponse(nr_parametri)

def operatie(request):
    try:
        a = int(request.GET.get("a", 0))
        b = int(request.GET.get("b", 0))
        op = request.GET.get("op", 0)    
        match op:
            case "sum":
                return HttpResponse(a + b)
            case "dif":
                return HttpResponse(a - b)
            case "mul":
                return HttpResponse(a * b)
            case "div":
                return HttpResponse(a / b)
            case _:
                return HttpResponse("ERROR Unknown operator")
    except:
            return HttpResponse("missing parameters")
        
def tabel(request):
    return render(request, "tabel.html")


def lista(request):
    # Lista de stringuri predefinite
    elemente_lista = ['mar', 'banana', 'portocala', 'capsuna', 'kiwi']

    # Preia parametrii 'cuvinte' din URL, dacă există
    cuvinte_colorate = request.GET.getlist('cuvinte')

    # Transmite lista și cuvintele colorate către template
    return render(request, 'lista.html', {'elemente_lista': elemente_lista, 'cuvinte_colorate': cuvinte_colorate})

def adunare_numere(request, userInput:str):
    global ACCESS_COUNT
    global MYSUMA
    ACCESS_COUNT += 1
    res = re.search(r'\d+', userInput)
    if res:
        MYSUMA += int(res.group())
    return HttpResponse(f"Numarul de cereri este{ACCESS_COUNT} si suma este {MYSUMA}")

def afisare_liste(request):
    parameters = request.GET
    html_output = ""

    for param in parameters:
        html_output += f"<h1> {param} </h1>"
        html_output += f"<ul>"
        for val in parameters.getlist(param):
            html_output += f"<li> {val} </li>"
        html_output += f"</ul>"
    return HttpResponse(html_output) 

from django.http import HttpResponse
import re

# Inițializăm un contor global
counter = 0

def numara_nume(request, nume):
    global counter
    
    # Definim pattern-ul pentru validarea numelui
    pattern = r"^[A-Z][a-z]*(-[A-Z][a-z]*)?\+[A-Z][a-z]*$"
    
    # Verificăm dacă `nume` respectă formatul corect
    if re.match(pattern, nume):
        counter += 1
        return HttpResponse(f"Nume corect! Număr total de nume primite: {counter}")
    else:
        return HttpResponse("Nume incorect.")

def cauta_subsir(request, userInput):
    pattern  = r"[ab]+"
    res = re.search(pattern, userInput)
    if res:
        mySubstring = res.group()
        return HttpResponse(len(mySubstring))
    else:
        return HttpResponse("not found")
