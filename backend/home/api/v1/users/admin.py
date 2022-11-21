from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username", "phone_number", "first_name", "last_name", "is_superuser"]
    search_fields = ["first_name", "last_name", "phone_number"]
