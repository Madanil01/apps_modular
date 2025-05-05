from django.contrib import admin
from .models import Module
from role.models import Role, UserDetails
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active')
    list_filter = ('is_active',)

    from .models import Role, UserDetails

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'module_name', 'access']
    search_fields = ['name', 'module_name']

@admin.register(UserDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    search_fields = ['user__username', 'role']
