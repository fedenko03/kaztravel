import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse

def main(request):
    return render(request, 'main.html')

def login_attempt(request):
    if request.user.is_authenticated:
        return redirect('/filter')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not username == 'admin' and not profile_obj.is_verified: #1111
            messages.success(request, 'Profile is not verified. Check your email.')
            return redirect('/login')

        user = authenticate(username = username, password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')

        login(request, user)
        return redirect('/filter')

    return render(request, 'login.html')


def register_attempt(request):
    if request.user.is_authenticated:
        return redirect('/filter')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.error(request, 'This username is already in use.')
                return redirect('/register')

            if username == '':
                messages.error(request, 'Incorrect username.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.error(request, 'This email is already in use.')
                return redirect('/register')

            user_obj = User(username = username, email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, username = username, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token, username)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')

def send_mail_after_registration(email, token, nick):
    subject = '[KazTravel] Your accounts need to be verified'
    message = f'{nick}, please verify your email address! \nTo complete your signup, please verify your email address by clicking on the link below:\n\nhttp://127.0.0.1:8000/verify/{token}\nIf it is not you who have registered, do not follow the link!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required(login_url='/login/')
def rating(request):
    template = 'rating.html'
    context = {
        'list_places': Places.objects.all().order_by('-id')[:5]
    }
    return render(request, template, context)


@login_required(login_url='/login/')
def filter(request):
    template = 'filter.html'
    context = {
        'places': Places.objects.all()
    }
    return render(request, template, context)

def token_send(request):
    if request.user.is_authenticated:
        return redirect('/filter')
    return render(request, 'token_send.html')


def logout_user(request):
    logout(request)
    return redirect('login_attempt')

def success(request):
    return render(request, 'success.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/filter')

def description(request):
    return render(request, 'description.html')

