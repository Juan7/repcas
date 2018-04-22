from django.shortcuts import render

# Create your views here.


def home(request):
    context = {}
    return render(request, 'main/home.html', context)


def app(request):
    client_pk = '1'
    return render(request, 'main/app/app.html', locals())
