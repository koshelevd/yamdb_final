"""Serializers of the 'users' app."""
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import YamdbUser


class UserSerializer(serializers.ModelSerializer):
    """
    'ModelSerializer' for 'users.models.YamdbUser' objects.
    """

    email = serializers.EmailField(
        validators=(UniqueValidator(queryset=YamdbUser.objects.all()),),
        required=True
    )

    class Meta:
        """Adds meta-information."""

        fields = ('first_name', 'last_name', 'username', 'email', 'bio',
                  'role')
        model = YamdbUser
