from django.contrib import admin
from .models.application import Application, ApplicationVersion, TenantInstallation

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'created_at')
    search_fields = ('name', 'code')
    list_filter = ('status',)

@admin.register(ApplicationVersion)
class ApplicationVersionAdmin(admin.ModelAdmin):
    list_display = ('application', 'version_number', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('application__name', 'version_number')

@admin.register(TenantInstallation)
class TenantInstallationAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'version', 'status', 'route_path', 'created_at')
    list_filter = ('status',)
    search_fields = ('tenant__name', 'version__application__name')
