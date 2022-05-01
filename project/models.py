from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='user')
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


Type = [
    ('hotel', 'hotel'),
    ('park', 'park'),
    ('museum', 'museum'),
    ('shop', 'shop')
]

City = [
    ('Nur-Sultan', 'Nur-Sultan'),
    ('Almaty', 'Almaty'),
    ('Aktobe', 'Aktobe'),
    ('Almaty obl', 'Almaty obl'),
    ('Atyrau', 'Atyrau'),
    ('Kostanay', 'Kostanay')
]

class Places(models.Model):

    name = models.TextField(verbose_name='Name:', max_length=300)
    description = models.TextField(verbose_name='Description:', max_length=1000)
    price = models.TextField(verbose_name='Price:', max_length=50)
    city = models.CharField(verbose_name='City', choices=City, max_length=40)
    type = models.CharField(verbose_name='Type', choices=Type, max_length=40)
    pic = ImageField(verbose_name='Picture', null=True, blank=True, max_length=100, upload_to='images/places')
