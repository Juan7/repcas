from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    context = {}
    return render(request, 'main/index.html', context)


def promotions(request):
    context = {}
    return render(request, 'main/promociones.html', context)


@login_required
def app(request):
    return render(request, 'main/app/app.html', locals())
