from django.contrib import admin

# Register your models here.
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display=['first_name','email','mobile','is_superuser']
admin.site.register(User,UserAdmin)