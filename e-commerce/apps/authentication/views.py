from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer


@extend_schema(tags=["auth"])
class RegistrationAPIView(APIView):
    """
    Register a new user.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @extend_schema(
        request=serializer_class, responses=UserSerializer, summary="Register a new user."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["auth"])
class LoginAPIView(APIView):
    """
    Login an existing user.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(
        request=serializer_class, responses=UserSerializer, summary="Login an existing user."
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["auth"], summary="Retrieve and update user information.")
class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Retrieve and update user information.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(request=serializer_class, responses=UserSerializer)
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializer_class, responses=UserSerializer)
    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
