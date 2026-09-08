from django.contrib import admin
from .models import Energy, EnergyHistory


@admin.register(Energy)
class EnergyAdmin(admin.ModelAdmin):
    list_display   = ('source', 'power_output', 'energy_today', 'energy_week', 'energy_month', 'efficiency', 'peak_power', 'timestamp')
    list_filter    = ('source',)
    readonly_fields = ('timestamp',)
    ordering       = ('source',)


@admin.register(EnergyHistory)
class EnergyHistoryAdmin(admin.ModelAdmin):
    list_display = ('source', 'date', 'energy', 'timestamp')
    list_filter  = ('source', 'date')
    ordering     = ('-date', 'source')
