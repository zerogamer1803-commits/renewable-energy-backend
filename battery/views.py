from django.http import JsonResponse
from .models import Battery, BatteryHistory


def battery_list(request):
    """GET /api/battery/ — current readings for all battery units."""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    batteries = Battery.objects.all()

    data = []
    for b in batteries:
        data.append({
            'id':                   b.id,
            'battery_id':           b.battery_id,
            'capacity':             b.capacity,
            'stored_energy':        b.stored_energy,
            'battery_level':        b.battery_level,
            'voltage':              b.voltage,
            'current':              b.current,
            'temperature':          b.temperature,
            'health':               b.health,
            'status':               b.status,
            'charging_power':       b.charging_power,
            'energy_received_today': b.energy_received_today,
            'energy_supplied_today': b.energy_supplied_today,
            'charge_cycles':        b.charge_cycles,
            'last_full_charge':     b.last_full_charge.isoformat() if b.last_full_charge else None,
            'timestamp':            b.timestamp.isoformat(),
        })

    return JsonResponse({'count': len(data), 'data': data})


def battery_history(request):
    """GET /api/battery/history/?battery_id=BAT-001&limit=24"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    battery_id = request.GET.get('battery_id')
    limit      = int(request.GET.get('limit', 24))

    qs = BatteryHistory.objects.select_related('battery').order_by('-timestamp')
    if battery_id:
        qs = qs.filter(battery__battery_id=battery_id)
    qs = qs[:limit]

    data = []
    for h in qs:
        data.append({
            'id':           h.id,
            'battery_id':   h.battery.battery_id,
            'battery_level': h.battery_level,
            'temperature':  h.temperature,
            'timestamp':    h.timestamp.isoformat(),
        })

    return JsonResponse({'count': len(data), 'data': data})
