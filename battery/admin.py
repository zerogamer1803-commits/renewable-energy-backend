from django.contrib import admin
from .models import Battery, BatteryHistory


@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display    = ('battery_id', 'battery_level', 'voltage', 'current', 'temperature', 'health', 'status', 'charging_power', 'timestamp')
    list_filter     = ('status',)
    readonly_fields = ('timestamp',)
    ordering        = ('battery_id',)


@admin.register(BatteryHistory)
class BatteryHistoryAdmin(admin.ModelAdmin):
    list_display = ('battery', 'battery_level', 'temperature', 'timestamp')
    list_filter  = ('battery',)
    ordering     = ('-timestamp',)
