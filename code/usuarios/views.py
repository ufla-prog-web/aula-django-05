from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = authenticate(username=usuario, password=senha)
        if user:
            login_django(request, user)
            return render(request, 'principal.html')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
            return render(request, 'login.html')

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else: #senão será via método "POST":
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se o usuário já está cadastrado
        user = User.objects.filter(username=usuario).first()
        if user:
            # Exibe uma mensagem de erro se o usuário já existir
            messages.error(request, 'Já existe um usuário com esse nome. Tente novamente.')
            return render(request, 'cadastro.html')
        else:
            # Cria e salva o usuário
            user = User.objects.create_user(username=usuario, email=email, password=senha)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return render(request, 'cadastro.html')

def logout(request):
    logout_django(request)
    return render(request, 'login.html')