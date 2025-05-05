from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.conf import settings
from role.models import *
from django.shortcuts import render, redirect
from django.contrib import messages
class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is None:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # Get user role
            try:
                role = user.role.access_level
            except:
                role = 'public'

            # Prepare response
            response = Response({
                'role': role,
                'access': access_token,
                'refresh': str(refresh)
            })

            # Set cookies
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            
            response.set_cookie(
                key='user_role',
                value=role,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=False,  # Diperlukan untuk dibaca oleh frontend
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            # Set CSRF token
            messages.success(request, 'Login successful')
            csrf.get_token(request)

            return response
            
        except Exception as e:
            messages.error(request, f"Failed to upgrade: {str(e)}")
    def get(self, request):
        return render(request, 'login.html')

class LogoutView(APIView):
    def post(self, request):
        try:
            response = redirect('login')  # Gantilah 'login' jika nama url-nya berbeda
            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                path='/',
                domain=settings.SESSION_COOKIE_DOMAIN if hasattr(settings, 'SESSION_COOKIE_DOMAIN') else None
            )
            # messages.success(request, 'Logout successful')
            return response
            
        except Exception as e:
            messages.error(request, f"Failed to logout: {str(e)}")
    
v_login = LoginView.as_view()
v_logout = LogoutView.as_view()