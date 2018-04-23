from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    # import pdb; pdb.set_trace()
    context = {}
    print(request.profile)
    return render(request, 'main/home.html', context)


@login_required
def app(request):
    return render(request, 'main/app/app.html', locals())
