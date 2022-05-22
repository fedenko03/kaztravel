from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=25, default='user')
    firstname = models.CharField(max_length=25, default='firstname', blank=False)
    lastname = models.CharField(max_length=25, default='lastname', blank=False)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = ImageField(verbose_name='Photo', null=True, max_length=100, upload_to='images/avatars', default='images/avatars/user.webp')

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
    recommend_1 = models.BooleanField(default=False)
    recommend_2 = models.BooleanField(default=False)
    pic = ImageField(verbose_name='Picture', null=True, blank=True, max_length=100, upload_to='images/places')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Place'
        verbose_name_plural = 'Places'


RATE_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
]


class Comments(models.Model):

    place = models.ForeignKey(Places, on_delete=models.CASCADE, verbose_name='Place', blank=True, null=True, related_name='comments_places')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author', blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Review:')
    rating = models.PositiveSmallIntegerField(verbose_name='Rating', choices=RATE_CHOICES)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Favorite(models.Model):
    places = models.ManyToManyField(Places)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark_user')