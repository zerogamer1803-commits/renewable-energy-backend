from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def api_root(request):
    """Quick health-check - confirms the backend is running."""
    return JsonResponse({
        'status': 'ok',
        'message': 'Renewable Energy Dashboard - Django REST API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'energy': '/api/energy/',
            'energy_history': '/api/energy/history/',
            'battery': '/api/battery/',
            'battery_history': '/api/battery/history/',
            'streetlights': '/api/street-lights/',
            'streetlights_history': '/api/street-lights/history/',
            'faults': '/api/faults/',
            'dashboard': '/api/dashboard/',
            'environment': '/api/environment/',
        },
    })


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', api_root, name='api-root'),

    path('api/energy/',  include('energy.urls')),
    path('api/battery/',      include('battery.urls')),
    path('api/street-lights/', include('streetlights.urls')),
    path('api/dashboard/',     include('dashboard.urls')),
]