import datetime

from django.core.exceptions import ValidationError

from rest_framework import serializers


def custom_slug_validation(data, model):
    category = model.objects.filter(slug=data).exists()
    if category:
        raise serializers.ValidationError(
            {'slug': 'This slug already exists'})
    return data


def max_year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            '%(value)s is not a correcrt year!',
            params={'value': value},
        )
