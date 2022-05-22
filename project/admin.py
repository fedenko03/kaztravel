from django.contrib import admin
from project.models import Profile, Places, Comments, Favorite
# Register your models here.


@admin.register(Profile)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("user", "username")
    search_fields = ("username__startswith",)


@admin.register(Places)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "city", "price")
    search_fields = ("name__startswith",)


@admin.register(Comments)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("author", "place", "rating")
    list_filter = ("place",)
    search_fields = ("place__startswith",)


# admin.site.register(Bookmark)
@admin.register(Favorite)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user']
