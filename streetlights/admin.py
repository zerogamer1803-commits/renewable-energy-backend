from django.contrib import admin
from .models import StreetLight, StreetLightHistory, Fault


@admin.register(StreetLight)
class StreetLightAdmin(admin.ModelAdmin):
    list_display    = ('light_id', 'location', 'status', 'state', 'power', 'voltage', 'fault', 'communication_status', 'last_updated')
    list_filter     = ('status', 'state', 'location', 'communication_status')
    search_fields   = ('light_id', 'location', 'fault')
    readonly_fields = ('last_updated',)
    ordering        = ('light_id',)


@admin.register(StreetLightHistory)
class StreetLightHistoryAdmin(admin.ModelAdmin):
    list_display = ('street_light', 'state', 'power', 'timestamp')
    list_filter  = ('state', 'street_light')
    ordering     = ('-timestamp',)


@admin.register(Fault)
class FaultAdmin(admin.ModelAdmin):
    list_display  = ('street_light', 'fault_type', 'severity', 'resolved', 'created_at', 'resolved_at')
    list_filter   = ('fault_type', 'severity', 'resolved')
    search_fields = ('street_light__light_id', 'message')
    ordering      = ('-created_at',)
