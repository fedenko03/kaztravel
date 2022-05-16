from django.contrib import admin
from project.models import Profile, Places
# Register your models here.


admin.site.register(Profile)

@admin.register(Places)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "city", "price")
    search_fields = ("name__startswith",)
