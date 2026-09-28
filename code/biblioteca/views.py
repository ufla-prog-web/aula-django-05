from django.http import HttpResponse
from django.template import loader
from .models import Livro
from .models import TCC
from django.contrib.auth.decorators import login_required

def principal(request):
    template = loader.get_template('principal.html')
    return HttpResponse(template.render({}, request))

def livros(request): 
    livros = Livro.objects.all().values()
    context = {
        'livros': livros
    }
    template = loader.get_template('livros.html')
    return HttpResponse(template.render(context, request))

def tccs(request):
    tccs = TCC.objects.all().values()
    context = {
        'tccs': tccs,
    }
    template = loader.get_template('tccs.html')
    return HttpResponse(template.render(context, request))

def tcc_detalhes(request, id):
    tcc = TCC.objects.get(id=id)
    context = {
        'tcc': tcc,
    }
    template = loader.get_template('tcc_detalhes.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url="/auth/login")
def dashboard(request):
    qtdLivros = Livro.objects.count()
    qtdTCCs = TCC.objects.count()
    context = {
        'labels': ['Livros', 'TCCs'],
        'data': [qtdLivros, qtdTCCs]
    }
    template = loader.get_template('dashboard.html')
    return HttpResponse(template.render(context, request))