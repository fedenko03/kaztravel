from django.urls import path
from .views import *

urlpatterns = [
    path('',  main, name="main"),
    path('register/', register_attempt, name="register_attempt"),
    path('login/', login, name="login"),
    path('filter/', filter, name="filter")
]