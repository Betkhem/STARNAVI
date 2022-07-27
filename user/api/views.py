# from django.shortcuts import render
from rest_framework import generics
from user.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

# Create your views here.

class CreateUserAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LogInAPIView(APIView):
    def post(self, request):
        response = Response()
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            response.data = {
                "response": "Provide both username and password"
            }
            return response
        
        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(str(password)):
            raise AuthenticationFailed('Incorrect password!')

        user.last_login = datetime.datetime.utcnow()
        user.save(update_fields=['last_login'])

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token = token.decode('utf-8')

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "response": "Success",
            'jwt': token
        }
        return response


class UserActivityEndpointAPIView(APIView):
    def get(self, request, pk):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        user = User.objects.filter(pk=pk).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        response = Response()
        response.data = {
            "last_login": user.last_login
        }
        return response
