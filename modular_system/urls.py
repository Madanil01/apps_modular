"""
URL configuration for modular_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.views.generic import RedirectView
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),  # This line was missing
    # path('product/', include('product.urls')),
    path('module/', include('core.urls')),  # For your module manager
    path('', include('authentication.urls')),
    # path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=False)), 
]
# mapping = [
#     {
#         'module_name': 'product',
#         'url': 'product/',
#         'installed': True
#     }
# ]
def get_dynamic_urls():
    dynamic_urls = []
    if 'product' in settings.INSTALLED_APPS:
        dynamic_urls.append(path('product/', include('product.urls')))
    return dynamic_urls

urlpatterns += get_dynamic_urls()