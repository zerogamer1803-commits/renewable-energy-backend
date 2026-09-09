from django.http import JsonResponse
from energy.models import Energy
from battery.models import Battery
from streetlights.models import StreetLight


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

    total_energy = solar + footstep

    # Battery
    battery = Battery.objects.first()
    battery_level = battery.battery_level if battery else 0
    battery_temp = battery.temperature if battery else 0

    # Street Lights
    working = StreetLight.objects.filter(status='Working').count()
    non_working = StreetLight.objects.exclude(status='Working').count()
    lights_on = StreetLight.objects.filter(state='ON').count()
    lights_off = StreetLight.objects.filter(state='OFF').count()

    # CO2 and Cost Savings
    co2_saved = total_energy * (12.4 / 18.7)
    cost_saved = total_energy * (185.0 / 18.7)

    return JsonResponse({
        'solar_energy': round(solar, 2),
        'footstep_energy': round(footstep, 2),
        'total_renewable_energy': round(total_energy, 2),
        'battery_level': battery_level,
        'battery_temperature': battery_temp,
        'working_lights': working,
        'non_working_lights': non_working,
        'lights_on': lights_on,
        'lights_off': lights_off,
        'co2_saved': round(co2_saved, 2),
        'cost_saved': round(cost_saved, 2),
    })