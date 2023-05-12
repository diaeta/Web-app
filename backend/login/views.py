# views.py

from django.contrib.auth import authenticate
from rest_framework import permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from .models import UserProfile
from .serializers import UserSerializer, LoginUserSerializer
from rest_framework import status


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        try:
            token_instance, token_key = AuthToken.objects.create(user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token_key
        })
