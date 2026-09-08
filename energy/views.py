from django.http import JsonResponse
from .models import Energy, EnergyHistory


def energy_list(request):
    """Return current solar and footstep energy data."""
    if request.method != 'GET':
        return JsonResponse({'error': 'GET method required'}, status=405)

    data = []

    for energy in Energy.objects.all():
        data.append({
            'source': energy.source,
            'power_output': energy.power_output,
            'energy_today': energy.energy_today,
            'energy_week': energy.energy_week,
            'energy_month': energy.energy_month,
            'efficiency': energy.efficiency,
            'peak_power': energy.peak_power,
            'timestamp': energy.timestamp.isoformat(),
        })

    return JsonResponse({
        'count': len(data),
        'data': data
    })


def energy_history(request):
    """Return historical energy generation data."""
    if request.method != 'GET':
        return JsonResponse({'error': 'GET method required'}, status=405)

    records = EnergyHistory.objects.all()

    data = []

    for record in records:
        data.append({
            'source': record.source,
            'energy': record.energy,
            'date': record.date.isoformat(),
            'timestamp': record.timestamp.isoformat(),
        })

    return JsonResponse({
        'count': len(data),
        'data': data
    })