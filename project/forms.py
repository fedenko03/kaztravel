import textwrap

from django import forms
from .models import Comments, Profile
from django.forms import Textarea


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text', 'rating')

    text = forms.CharField(
        max_length=200,
        min_length=35,
        widget=forms.Textarea(attrs={'name': 'message',
                                     'rows': '5',
                                     'placeholder': 'Message',
                                     'class': 'form-control mb-3'})
    )

    rating = forms.ChoiceField(
        choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')],
        widget=forms.Select(attrs={'label': 'Rating',
                                   'class': 'mb-3 form-select'})
    )


class AvatarForm(forms.Form):
    image = forms.ImageField()
