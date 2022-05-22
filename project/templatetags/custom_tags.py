from django import template
register = template.Library()
from project.models import Profile

@register.simple_tag
def get_photo(username):
    obj = Profile.objects.filter(username=username).first()
    return obj.avatar.url