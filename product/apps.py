from django.apps import AppConfig
from django.db.models.signals import pre_delete

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    
    def ready(self):
        # Auto-register URLs saat modul aktif
        try:
            from .urls import urlpatterns
            from django.urls import include, path
            from modular_system.urls import urlpatterns as root_urls
            
            if not any(p.pattern == 'product/' for p in root_urls):
                root_urls.append(path('product/', include('product.urls')))
        except ImportError:
            pass