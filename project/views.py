from django.shortcuts import redirect, render, HttpResponse
from .models import *

def main(request):
    return render(request, 'main.html')

def login(request):
    return render(request, 'login.html')

def register_attempt(request):
    return render(request, 'register.html')

def filter(request):
    template = 'filter.html'
    context = {
        'places': Places.objects.all()
    }
    return render(request, template, context)

