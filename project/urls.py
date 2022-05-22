from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

from kaztravel import settings
from .views import *

urlpatterns = [
    path('',  main, name="main"),
    path('register/', register_user, name="register_user"),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('token', token_send, name="token_send"),
    path('verify/<auth_token>', verify, name="verify"),
    path('success', success, name='success'),
    path('places/', places, name="places"),
    path('places/place<int:pk>', place_detail, name="place_detail"),
    path('comment<int:comment_id>/delete', delete_com, name='delete_com'),
    path('<int:pk>/favorite', favorite, name='place_favorite'),
    path('profile', profile, name='profile'),
    path('recommendations', recommendations, name="recommendations"),
    path('rating', rating, name='rating'),
    # path('error', e)
    # path('recovery', recovery, name="recovery"),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)