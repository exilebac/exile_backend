from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        'username', 'email', 'full_name', 'phone_number',
        'birth_date', 'profession', 'speciality',
        'country', 'city', 'is_active', 'is_staff'
    ]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'full_name', 'phone_number', 'birth_date',
            'profession', 'speciality', 'country', 'city',
            'last_login_time', 'last_login_ip'
        )}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
