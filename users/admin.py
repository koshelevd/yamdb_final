"""Application 'users' admin page configuration."""
from django.contrib import admin

from .models import YamdbUser


@admin.register(YamdbUser)
class YamdbUserAdmin(admin.ModelAdmin):
    """Manage users."""

    list_display = (
        'pk',
        'role',
        'username',
        'first_name',
        'last_name',
        'email',
        'bio',
    )
    search_fields = (
        'username',
        'email',
    )
    filter_fields = (
        'role',
    )
    empty_value_display = '-пусто-'
