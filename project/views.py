from django.shortcuts import redirect, render, HttpResponse


def main(request):
    return render(request, 'main.html')

def login(request):
    return render(request, 'login.html')

def register_attempt(request):
    return render(request, 'register.html')

def filter(request):
    return render(request, 'filter.html')

def description(request):
    return render(request, 'description.html')

