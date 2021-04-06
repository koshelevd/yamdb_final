"""View classes of the 'users' app."""
from uuid import uuid4

from django.core.mail import send_mail
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import BadRequest, ServerError
from .models import YamdbUser
from .permissions import IsAdmin
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Viewset for 'users.models.YamdbUser' model.
    """

    queryset = YamdbUser.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    @action(detail=False,
            methods=('get', 'patch'),
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        """Implement /users/me/ endpoint."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def api_user_create(request):
    """
    Create new user if request with 'email' parameter is posted.

    If parameter 'email' is specified then create new user with 'username'
    the same as email's login and random 'confirmation_code'.
    Send 'confirmation_code' to email specified.
    """
    try:
        email = request.data.get('email')
        username = email.split('@')[0]
        user, _ = YamdbUser.objects.get_or_create(
            username=username,
            email=email,
            confirmation_code=str(uuid4())
        )
    except AttributeError:
        raise ParseError
    except IntegrityError:
        raise BadRequest
    except Exception:
        raise ServerError

    message = ('Please confirm your registration with code: '
               f'{user.confirmation_code}')
    try:
        send_mail(
            subject='Verification code for YaMDB',
            message=message,
            from_email=None,
            recipient_list=(email,)
        )
    except Exception:
        raise ServerError

    return Response({'detail': 'Please confirm your email to obtain token'})


@api_view(['POST'])
@permission_classes([AllowAny])
def send_token(request):
    """Send token if confirmation code is valid."""
    confirmation_code = request.data.get('confirmation_code')
    if confirmation_code is None:
        raise BadRequest
    user = get_object_or_404(YamdbUser, confirmation_code=confirmation_code)
    refresh = RefreshToken.for_user(user)
    response = {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }
    return Response(response)
