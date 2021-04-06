from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title
from .validators import custom_slug_validation


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        exclude = ('id', )
        model = Category

    def validate_slug(self, data):
        return custom_slug_validation(data, Category)


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        exclude = ('id', )
        model = Genre

    def validate_slug(self, data):
        return custom_slug_validation(data, Genre)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class TitleSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(required=False)
    rating = serializers.FloatField(read_only=True)
    description = serializers.CharField(required=False)

    genre = serializers.SlugRelatedField(many=True,
                                         slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
            )
        model = Title

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            title.genre.add(genre)
        return title

    def to_representation(self, instance):
        representation = super(TitleSerializer,
                               self).to_representation(instance)

        # Present genres in a readable way
        title_genres = Genre.objects.filter(slug__in=representation['genre'])
        representation['genre'] = title_genres.values('name', 'slug')

        # present category in a readable way
        category = get_object_or_404(Category, slug=representation['category'])

        title_category = {'name': category.name, 'slug': category.slug}
        representation['category'] = title_category

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault())
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'title')
        model = Review

    def validate(self, data):
        current_user = self.context['request'].user
        if Review.objects.filter(
                title=self.context['title_id'], author=current_user
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение')
        return data
