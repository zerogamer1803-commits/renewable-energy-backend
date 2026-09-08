from django.http import JsonResponse
from .models import StreetLight, StreetLightHistory, Fault


def street_light_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    lights = StreetLight.objects.all()
    data = [
        {
            'light_id':             l.light_id,
            'location':             l.location,
            'status':               l.status,
            'state':                l.state,
            'power':                l.power,
            'voltage':              l.voltage,
            'fault':                l.fault,
            'communication_status': l.communication_status,
            'brightness':           l.brightness,
            'last_updated':         l.last_updated.isoformat(),
        }
        for l in lights
    ]
    return JsonResponse({'count': len(data), 'data': data})


def street_light_history(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    records = StreetLightHistory.objects.select_related('street_light').all()
    data = [
        {
            'light_id':  r.street_light.light_id,
            'state':     r.state,
            'power':     r.power,
            'timestamp': r.timestamp.isoformat(),
        }
        for r in records
    ]
    return JsonResponse({'count': len(data), 'data': data})


def fault_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    faults = Fault.objects.select_related('street_light').all()
    data = [
        {
            'light_id':    f.street_light.light_id,
            'fault_type':  f.fault_type,
            'severity':    f.severity,
            'message':     f.message,
            'resolved':    f.resolved,
            'created_at':  f.created_at.isoformat(),
            'resolved_at': f.resolved_at.isoformat() if f.resolved_at else None,
        }
        for f in faults
    ]
    return JsonResponse({'count': len(data), 'data': data})
