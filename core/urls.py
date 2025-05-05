from django.urls import path
from . import views

urlpatterns = [
    path('', views.module_manager, name='module-manager'),
    path('install/<str:module_name>/', views.install_module, name='install-module'),
    path('uninstall/<str:module_name>/', views.uninstall_module, name='uninstall-module'),
    path('upgrade-page/<str:module_name>/', views.upgrade_module, name='upgrade-module-page'),
    path('apply-upgrade-module/<str:module_name>/', views.apply_upgrade_module, name='apply-upgrade-module'),

]