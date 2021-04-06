import django_filters
from django_filters import filters

from .models import Title


class TitleFilter(django_filters.FilterSet):
    category = filters.CharFilter(
        field_name='category__slug',
        lookup_expr='iexact')
    genre = filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='contains')
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='contains')

    class Meta:
        model = Title
        fields = [
            'category',
            'genre',
            'name',
            'year',
            ]
