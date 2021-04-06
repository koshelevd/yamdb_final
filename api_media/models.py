from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from .validators import max_year_validator

User = get_user_model()


class Category(models.Model):
    """ Category model represents different types of media with can be
    reviewed, e.g. movies, books, etc """
    name = models.CharField(
        max_length=30,
        null=False,
        unique=True,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=30,
        null=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Genre(models.Model):
    """ Genre model represents different types of genres """
    name = models.CharField(
        max_length=30,
        null=False,
        unique=True,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=30,
        null=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'


class Title(models.Model):
    """ Model represents titles description, including genre and category"""
    name = models.CharField(
        max_length=30,
        null=False,
        unique=True,
        verbose_name='Название произведения',
    )
    year = models.PositiveIntegerField(
        null=True,
        db_index=True,
        validators=[max_year_validator],
        verbose_name='Год релиза',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Категория',
    )

    class Meta():
        verbose_name_plural = 'Тайтлы'
        verbose_name = 'Тайтл'


class Review(models.Model):
    """Creates a 'model.Review' object for a 'model.Title' object"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст',
    )
    pub_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Значение должно быть больше 1'),
            MaxValueValidator(10, message='Значение должно быть больше 10')
        ],
        verbose_name='Оценка',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')]
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Creates a 'model.Comment' object for a 'model.Review' object"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст',
    )
    pub_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
