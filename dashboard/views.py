from django.http import JsonResponse
from django.utils import timezone
from energy.models import Energy
from battery.models import Battery
from streetlights.models import StreetLight
from .models import EnvironmentalStats


def dashboard_summary(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # Energy
    try:
        solar = Energy.objects.get(source='Solar').energy_today
    except Energy.DoesNotExist:
        solar = 0.0

    try:
        footstep = Energy.objects.get(source='Footstep').energy_today
    except Energy.DoesNotExist:
        footstep = 0.0

    # Battery
    battery = Battery.objects.first()
    battery_level = battery.battery_level if battery else 0
    battery_temp  = battery.temperature   if battery else 0

    # Street Lights
    working     = StreetLight.objects.filter(status='Working').count()
    non_working = StreetLight.objects.exclude(status='Working').count()
    lights_on   = StreetLight.objects.filter(state='ON').count()
    lights_off  = StreetLight.objects.filter(state='OFF').count()

    # Environmental Stats
    try:
        env = EnvironmentalStats.objects.get(date=timezone.localdate())
        co2_saved  = env.co2_saved
        cost_saved = env.cost_saved
    except EnvironmentalStats.DoesNotExist:
        co2_saved  = 0.0
        cost_saved = 0.0

    return JsonResponse({
        'solar_energy':           round(solar, 2),
        'footstep_energy':        round(footstep, 2),
        'total_renewable_energy': round(solar + footstep, 2),
        'battery_level':          battery_level,
        'battery_temperature':    battery_temp,
        'working_lights':         working,
        'non_working_lights':     non_working,
        'lights_on':              lights_on,
        'lights_off':             lights_off,
        'co2_saved':              round(co2_saved, 2),
        'cost_saved':             round(cost_saved, 2),
    })
