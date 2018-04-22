from django.shortcuts import render

# Create your views here.


def home(request):
    context = {}
    print(request.profile)
    return render(request, 'main/home.html', context)
