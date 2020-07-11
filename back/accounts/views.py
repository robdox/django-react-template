import logging

from django.contrib.auth import password_validation
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
    lookup_value_regex = "[^/]+"
    permission_classes = [IsAuthenticated]

    def update(self, request, email=None):
        obj = self.get_object()

        if obj != request.user:
            raise PermissionDenied

        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, email=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def destroy(self, request, email=None):
        obj = self.get_object()

        if obj != request.user:
            raise PermissionDenied

        obj.is_active = False
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Essentially retrieve but i just want to check their token in cookies
    # The react will remove it if it is invalid and log them out
    @action(detail=False, methods=["get"])
    def verify(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ConfirmEmailView(APIView):  # pragma: nocover
    def post(self, request, key):
        password = request.data["password"]
        try:
            user = User.objects.get(verification_key=key.strip())
            try:
                password_validation.validate_password(password)
            except ValidationError as e:
                logger.warning(e)
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"text": e})

            user.set_password(password)
            user.save()
            token = Token.objects.get_or_create(user=user)

            User.objects.filter(verification_key=key.strip()).update(
                email_verified=True, verification_key=""
            )
            return Response(status=status.HTTP_200_OK, data={"key": token[0].key})
        except User.DoesNotExist as e:
            logger.warning(e)
            return Response(
                status=status.HTTP_401_UNAUTHORIZED, data={"text": ["Invalid Token"]}
            )


class ResetPasswordView(APIView):  # pragma: nocover
    def post(self, request, email):
        user = User.objects.get(email=email)
        user.send_confirmation()
        return Response()
