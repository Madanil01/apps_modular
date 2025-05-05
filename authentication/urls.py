# product/urls.py
from django.urls import path
from .views import v_login, v_logout

urlpatterns = [
    path('login/', v_login, name='login'),
    path('logout/', v_logout, name='logout'),
    # path('delete/<int:pk>/', views.delete_product, name='delete-product'),
]