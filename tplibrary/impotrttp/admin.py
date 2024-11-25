from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AddTP, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AddTP)
