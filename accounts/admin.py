from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active", "age", "phone_number")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        (None, {
            "fields": (
                "username", "password",
                "first_name", "last_name", "email",
                "phone_number", "age", "gender",
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
                "last_login", "date_joined",
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "first_name", "last_name", "email",
                "phone_number", "gender", "age",
                "password1", "password2", "is_active", "is_staff"
            ),
        }),
    )

    search_fields = ("email", "username")
    ordering = ("email",)



