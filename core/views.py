from django.shortcuts import render, redirect
from django.contrib import messages
from importlib import import_module
from django.conf import settings
import importlib
import sys
from product.install import install
from django.views.decorators.csrf import csrf_exempt
from .models import Module
import jwt
from role.models import *
from django.contrib.auth.models import User
from django.apps import apps
from django.db.models.fields import NOT_PROVIDED
from core.models import DynamicField
from django.db import transaction
from product.models import Product
def module_manager(request):
    try:
        installed_modules = []
        available_modules = [] 
        user_data = user_data_func(request)

        # Scan installed modules
        # for app in settings.INSTALLED_APPS:
        #     if app.startswith(''):
        #         module_name = app.split('.')[-1]
                
        #         installed_modules.append({
        #             'name': module_name,
        #             'version': getattr(importlib.import_module(app), '__version__', '1.0')
        #         })
        installed_modules = Module.objects.filter(is_active=True).all()
        available_modules = Module.objects.filter(is_active=False).all()
        # Scan available modules (example)
        # available_modules = [
            
        #     # {'name': 'inventory', 'version': '1.0'}
        # ]
        # messages.success(request, "Module manager loaded!")
        return render(request, 'core/module_manager.html', {
            'installed_modules': installed_modules,
            'available_modules': available_modules,
            'user': user_data
        })
    except Exception as e:
        messages.error(request, str(e))
        return redirect('module-manager')
@csrf_exempt
def install_module(request, module_name):
    try:
        with transaction.atomic():
            
            module = import_module(f"{module_name}.install")
            moduleObj = Module.objects.get(name=module_name)
            moduleObj.is_active = True
            moduleObj.save()
            if hasattr(module, 'install'):
                module.install()
            
            if f"{module_name}" not in settings.INSTALLED_APPS:
                new_installed_apps = list(settings.INSTALLED_APPS) + [f"{module_name}"]
                settings.INSTALLED_APPS = new_installed_apps
            
            messages.success(request, f"Module {module_name} v{moduleObj.version} installed!")
        
    except Exception as e:
        messages.error(request, f"Install failed: {str(e)}")
    
    return redirect('module-manager')
@csrf_exempt
def uninstall_module(request, module_name):
    try:
        with transaction.atomic():
            module_path = f"{module_name}"
           
        
            try:
                module = import_module(f"{module_path}.uninstall")
        
                if hasattr(module, 'uninstall'):
                    
                    module.uninstall()
                
                Product.objects.all().delete()
                module = Module.objects.get(name=module_name)
                module.is_active = False
                module.save()
            except ImportError:
                raise Exception("Module not found or already uninstalled")
            
            if module_path in settings.INSTALLED_APPS: 
                settings.INSTALLED_APPS.remove(module_path)

            for key in list(sys.modules.keys()):
                if key.startswith(module_path):
                    del sys.modules[key]
            
            messages.success(request, f"Module {module_name} uninstalled successfully!")
    except Exception as e:
        messages.error(request, f"Failed to uninstall: {str(e)}")
    
    return redirect('module-manager')

def upgrade_module(request, module_name):
    try:
        with transaction.atomic():
            user_data = user_data_func(request)
            model = apps.get_model(module_name, module_name.capitalize())

            field_list = [
                {
                    'name': field.name,
                    'type': field.get_internal_type(),
                    'editable': field.editable,
                    'blank': field.blank,
                    'null': field.null,
                    'default': (
                        field.default if field.default != NOT_PROVIDED else None
                    ),
                    'is_dynamic': False,
                }
                for field in model._meta.get_fields()
                if not field.is_relation and field.concrete
            ]

            custom_fields = DynamicField.objects.filter(model_name=module_name.capitalize())
            for cf in custom_fields:
                field_list.append({
                    'id': cf.id,
                    'name': cf.field_name,
                    'type': cf.field_type,
                    'editable': True,
                    'blank': cf.blank,
                    'null': cf.nullable,
                    'default': cf.default,
                    'is_dynamic': True,
                })

            return render(request, 'core/upgrade_module.html', {
                'module_name': module_name,
                'user': user_data,
                'fields': field_list
            })
    except Exception as e:
        messages.error(request, f"Failed to upgrade: {str(e)}")
    
    return redirect('module-manager')
def apply_upgrade_module(request, module_name):
    try:
        with transaction.atomic():
            module = import_module(f"{module_name}.upgrade")
            
            rsp = module.upgrade(request)
            if rsp ==False:
                raise Exception("Failed to upgrade")
            dataModule = Module.objects.get(name=module_name)
            dataModule.version = str(int(dataModule.version) + 1)
            dataModule.save()
            messages.success(request, f"Module {module_name} upgraded successfully!")
    except Exception as e:
        messages.error(request, f"Failed to upgrade: {str(e)}")
    
    return redirect('upgrade-module-page', module_name=module_name)

def user_data_func(request):
    token = request.COOKIES.get('access_token')  # Sesuaikan key cookie
    # print(token)
    user_detail = None
    if token:
        try:
            decoded = jwt.decode(
                token,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[settings.SIMPLE_JWT['ALGORITHM']]
            )
           
            user_id = decoded.get('user_id')
            
            if user_id:
                
                user = User.objects.get(id=user_id)
                if user.is_superuser:
                    data = {
                        'username': 'Admin',
                        'first_name':'Admin',
                        'last_name': user.last_name,
                        'role': 'superuser',
                        'is_authenticated': True,
                        'access': ['R', 'C', 'U', 'D'],
                        'role_name': 'superuser'
                    }
                    return data
                
                user_detail = UserDetails.objects.filter(user=user).first()
                
                # role_access = Role.objects.get(id=user_detail.role)
                data = {
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user_detail.role,
                    'is_authenticated': True,
                    'access': user_detail.role.access.split(','),
                    'role_name': user_detail.role.name
                }
            
            else:
                data = {
                    'username': None,
                    'role': None,
                    'is_authenticated': False,
                    'access': None
                }   
        except (jwt.DecodeError, jwt.ExpiredSignatureError, User.DoesNotExist, UserDetails.DoesNotExist):
            data = {
                'username': None,
                'role': None,
                'is_authenticated': False,
                'access': None
            }
    return data