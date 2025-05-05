from django.shortcuts import redirect
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin

class TokenValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        
        token = request.COOKIES.get('access_token')

        if path.startswith('/login'):
            if token:
                try:
                    AccessToken(token)  # Valid token
                    return redirect('/module')  # Jika sudah login, arahkan ke module
                except TokenError:
                    pass  # Token invalid, biarkan tetap ke /login
            return  # Tidak ada token, tetap lanjut ke /login

        elif path.startswith('/logout') or path.startswith('/admin') or path.startswith('/static'):
            return  # Allow access tanpa cek token

        # Untuk halaman lain: harus punya token valid
        if token:
            try:
                AccessToken(token)  # valid
                return  # lanjut ke halaman yang diminta
            except TokenError:
                return redirect('/login')  # token invalid/expired
        else:
            return redirect('/login')  # tidak ada token