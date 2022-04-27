from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from kaztravel import settings
from .views import *

urlpatterns = [
    path('',  main, name="main"),
    path('register/', register_attempt, name="register_attempt"),
    path('login/', login, name="login"),
    path('filter/', filter, name="filter")
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)