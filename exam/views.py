from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.core.mail import send_mail, mail_admins

# Create your views here.

def home(request):
    return HttpResponse('Primul raspuns')

def afisareProfesori(request):
    profesori = Profesor.objects.all()
    return render(request, 'profesori.html', {'profesori': profesori})
    
def afisareMaterii(request, code):
    # Codul este de forma Nume_Prenume
    codeNames = code.split('_')
    nume = codeNames[0]
    prenume = codeNames[1]

    profesor = Profesor.objects.filter(nume__iexact=nume, prenume__iexact=prenume).first()
    materii = Materie.objects.filter(profesor=profesor)

    return render(request, 'materii.html', {'profesor': profesor, 'materii':materii})

def adaugaMaterie(request):
    if request.method == 'POST':
        form = MaterieForm(request.POST)
        if form.is_valid():
            myMaterie = form.save(commit=False)
            if len(myMaterie.titlu) > 10:
                # Send an email to the admins
                mail_admins('Prioteasa Liviu', 'A fost trmis un titlu cu mai mult de 10 caractere', fail_silently=False, connection=None, html_message=None)
            myMaterie.save()
            print('FORM TRIMIS CU SUCCES' )
            return redirect('/exam/')
        else:
            print('DEBUG: intra in form is not valid', form.errors)
            return render(request, 'materie_form.html', {'form': form})                
    else:
        form = MaterieForm()
        print('DEBUG: intra in GET')
        return render(request, 'materie_form.html', {'form': form})        

