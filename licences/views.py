from django.shortcuts import render
from .models import Licence

def licence_expiree(request):
    return render(request, 'licences/licence_expiree.html')

def some_view(request):
    licence = Licence.objects.filter(active=True).first()
    context = {
        'licence': licence,
    }
    return render(request, 'base.html', context)