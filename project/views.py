import random
import string
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
from .forms import CommentForm, AvatarForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView


def main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not username == 'admin' and not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified. Check your email.')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')

        login(request, user)
        return redirect('/places')
    context = {
        'profile': Profile.objects.filter(username=request.user.username).first()
    }
    return render(request, 'main.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/places')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user = user_obj).first()

        if not username == 'admin' and not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified. Check your email.')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/login')

        login(request, user)
        return redirect('/places')

    return render(request, 'login.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('/places')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        print(password)

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'This username is already in use.')
                return redirect('/register')

            if username == '':
                messages.error(request, 'Incorrect username.')
                return redirect('/register')

            if User.objects.filter(email=email).first():
                messages.error(request, 'This email is already in use.')
                return redirect('/register')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, username=username, firstname=firstname, lastname=lastname,  auth_token=auth_token)
            profile_obj.save()
            send_email_after_registration(email, auth_token, username)
            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'register.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
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
        return redirect('/places')

def send_mail_recovery(email, token, nick):
    subject = '[KazTravel] Password Recovery'
    message = f'{nick}, To restore your password, follow the link: \n\nhttps://kazztravel.herokuapp.com/recovery/{token}\nIf it wasn\'t you, don\'t follow the link!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def recovery(request):
    if request.user.is_authenticated:
        return redirect('/places')
    message = ''
    if request.method == "POST":
        username = request.POST.get('username')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            message = 'User not found.'
        else:
            password_token = str(uuid.uuid4())
            profile_obj = Profile.objects.filter(username=username).first()
            profile_obj.auth_token = password_token
            profile_obj.save()
            send_mail_recovery(user_obj.email, password_token, username)
            messages.success(request, 'A link has been sent to your email address.')
            return redirect('/login')

    context = {
        'profile': Profile.objects.filter(username=request.user.username).first(),
        'message': message
    }
    return render(request, 'recovery.html', context)


def recovery_confirm(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            letters = string.ascii_lowercase + string.digits
            new_password = ''.join(random.choice(letters) for i in range(8))
            profile_obj.auth_token = str(uuid.uuid4())
            profile_obj.save()

            user_obj = User.objects.get(username=profile_obj.username)
            user_obj.set_password(new_password)
            user_obj.save()
            context = {
                'new_password': new_password
            }
            return render(request, 'recovery-confirm.html', context)
        else:
            messages.success(request, 'ERROR! Try again.')
            return redirect('/login')
    except Exception as e:
        messages.success(request, 'ERROR! Try again.')
        return redirect('/login')


def token_send(request):
    if request.user.is_authenticated:
        return redirect('/filter')
    return render(request, 'token_send.html')


def logout_user(request):
    logout(request)
    return redirect('login_user')


def success(request):
    if request.user.is_authenticated:
        return redirect('/places')
    return render(request, 'success.html')


def send_email_after_registration(email, token, nick):
    subject = '[KazTravel] Your accounts need to be verified'
    message = f'{nick}, please verify your email address! \nTo complete your signup, please verify your email address by clicking on the link below:\n\nhttps://kazztravel.herokuapp.com/verify/{token}\nIf it is not you who have registered, do not follow the link!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required(login_url='/login/')
def rating(request):
    template = 'rating.html'
    context = {
        'list_places': Places.objects.all().order_by('-visits')[:10],
        'profile': Profile.objects.filter(username=request.user.username).first()
    }
    return render(request, template, context)


@login_required(login_url='/login/')
def recommendations(request):
    context = {
        # 'places': Places.objects.filter(recommendations = "natural").all()
        'profile': Profile.objects.filter(username=request.user.username).first(),
        'places_1': Places.objects.filter(recommend_1='True').all()[:5],
        'places_2': Places.objects.filter(recommend_2='True').all()[:5]
    }
    return render(request, 'recommendations.html', context)


@login_required(login_url='/login/')
def places(request):
    template = 'places.html'
    context = {
        'places': Places.objects.all(),
        'profile': Profile.objects.filter(username=request.user.username).first()
    }
    return render(request, template, context)


@login_required(login_url='/login/')
def profile(request):
    message_pass = ''
    message_set = ''
    message_ava = ''
    if request.method == 'POST':
        if 'change_password' in request.POST:
            current_password_Checker = request.user.password
            current_password = request.POST.get('Current_password')
            new_password = request.POST.get('New_password')
            passwordcheck = check_password(current_password, current_password_Checker)

            if passwordcheck:
                user_obj = User.objects.get(username=request.user)
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, 'Password changed successfully. Please log in again.')
                return redirect('/login')
            else:
                message_pass = 'Error'

        if 'change_settings' in request.POST:
            new_firstname = request.POST.get('firstname')
            new_lastname = request.POST.get('lastname')

            profile_obj = Profile.objects.filter(username=request.user.username).first()
            profile_obj.firstname = new_firstname
            profile_obj.lastname = new_lastname
            profile_obj.save()
            message_set = 'Settings changed successfully.'

        if 'upload_avatar' in request.POST:
            form = AvatarForm(request.POST, request.FILES)
            if form.is_valid():
                m = Profile.objects.filter(username=request.user.username).first()
                m.avatar = form.cleaned_data['image']
                m.save()
                message_ava = 'Your profile photo has been updated'
            else:
                message_ava = 'Error'

    if Favorite.objects.filter(user=request.user).exists():
        favorites_data = Favorite.objects.get(user=request.user).places.all()
    else:
        favorites_data = ''

    context = {
        'favorites_data': favorites_data,
        'profile': Profile.objects.filter(username=request.user.username).first(),
        'message_pass': message_pass,
        'message_set': message_set,
        'message_ava': message_ava
    }
    return render(request, 'profile.html', context)


@login_required(login_url='/login/')
def place_detail(request, pk):
    place = get_object_or_404(Places, id=pk)
    place.visits += 1
    place.save()
    comment = Comments.objects.filter(place=pk)
    hasCommented = False

    if comment.filter(author=request.user).first():
        hasCommented = True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if not hasCommented:
            form = form.save(commit=False)
            form.author = request.user
            form.place = place
            form.save()
            return redirect(place_detail, pk)
    else:
        form = CommentForm()

    try:
        b, _ = Favorite.objects.get_or_create(user=request.user)
        if b.places.filter(id=pk).exists():
            isfavorites = 1
        else:
            isfavorites = 0
    except Exception as e:
        isfavorites = 0

    sum_rating = 0
    num_rating = 0

    for rating in comment:
        sum_rating += rating.rating
        num_rating += 1

    if sum_rating == 0:
        num_rating = 1

    return render(request, "place_detail.html",
                  {"place": place,
                   'profile': Profile.objects.filter(username=request.user.username).first(),
                   "comments": comment,
                   "hasCommented": hasCommented,
                   "isfavorites": isfavorites,
                   "rating": round(sum_rating/num_rating,2),
                   "form": form})


@login_required(login_url='/login/')
def delete_com(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    place_id = comment.place.id
    if request.user == comment.author:
        Comments.objects.get(id=comment_id).delete()
    return redirect(place_detail, place_id)


@login_required(login_url='/login/')
def favorite(request, pk):
    user = request.user
    place = get_object_or_404(Places, id=pk)

    try:
        b, created = Favorite.objects.get_or_create(user=user)
        if b.places.filter(id=pk).exists():
            b.places.remove(place)
        else:
            b.places.add(place)
        place.save()
        return redirect(place_detail, pk)
    except Exception as e:
        raise e





