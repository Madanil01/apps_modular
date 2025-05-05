from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.conf import settings
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
            role = getattr(user, 'role', None)
            role = role.access_level if role else 'public'

            # Build response
            response = Response({
                'role': role,
                'access': access_token,
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)

            # Set JWT cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=access_token,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            # Set a non-HTTP-only cookie for role
            response.set_cookie(
                key='user_role',
                value=role,
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=False,
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )

            # Trigger CSRF token generation
            csrf.get_token(request)
            messages.success(request, 'Login successful')

            return response

        except Exception as e:
            messages.error(request, f"Login failed: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        return render(request, 'login.html')


class LogoutView(APIView):
    def post(self, request):
        try:
            response = redirect('login')  # or your login URL name
            response.delete_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                path='/',
                domain=getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
            )
            messages.success(request, 'Logout successful')
            return response

        except Exception as e:
            messages.error(request, f"Logout failed: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
