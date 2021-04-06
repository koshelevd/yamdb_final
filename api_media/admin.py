from django.contrib import admin

from .models import Category, Genre, Review, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Manage genres."""

    list_display = (
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Manage categories."""

    list_display = (
        'name',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Manage titles."""

    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Manage reviews."""

    list_display = (
        'author',
        'title',
        'text',
        'score'
    )
    empty_value_display = '-пусто-'
