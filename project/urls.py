from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from kaztravel import settings
from .views import *

urlpatterns = [
    path('',  main, name="main"),
    path('register/', register_attempt, name="register_attempt"),
    path('login/', login, name="login"),
    path('filter/', filter, name="filter"),
    path('description/', description, name="description")
    path('login/', login_attempt, name="login_attempt"),
    path('logout/', logout_user, name="logout_user"),
    path('verify/<auth_token>', verify, name="verify"),
    path('success', success, name='success'),
    path('token', token_send, name="token_send"),
    path('filter/', filter, name="filter")
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)