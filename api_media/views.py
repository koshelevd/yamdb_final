from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters import rest_framework

from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import IsGetOrIsAdmin, IsGetOrPostOrAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    model = Category
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsGetOrIsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    model = Genre
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [IsGetOrIsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    model = Title
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializer
    permission_classes = [IsGetOrIsAdmin]
    pagination_class = PageNumberPagination
    filter_backends = (rest_framework.DjangoFilterBackend, )
    filterset_class = TitleFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]


class CommentViewSet(viewsets.ModelViewSet):
    """  A ViewSet for viewing and editing comments."""
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsGetOrPostOrAdmin, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    def get_review(self):
        """Extract review from a request."""
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self, *args, **kwargs):
        """Return comments of a review."""
        return self.get_review().comments.all().order_by('pk')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """  A ViwSet for viewing and editing reviews."""

    serializer_class = ReviewSerializer
    permission_classes = [IsGetOrPostOrAdmin, IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
    ]

    def get_queryset(self, *args, **kwargs):
        """Returns reviews of a title."""
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all().order_by('pk')

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title_id=title_id)

    def get_serializer_context(self):
        """Pass request attribute to serializer."""
        return {
            'request': self.request,
            'title_id': self.kwargs.get('title_id')
        }
