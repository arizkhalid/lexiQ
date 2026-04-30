# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import UserSerializer


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.pop("refresh")
        is_secure = not settings.DEBUG
        samesite = "None" if is_secure else "Lax"
        response.set_cookie(
            "refresh",
            refresh,
            httponly=True,
            secure=is_secure,
            samesite=samesite,
            max_age=7 * 24 * 3600,
        )
        return response


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data["refresh"] = request.COOKIES.get("refresh", "")
        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
