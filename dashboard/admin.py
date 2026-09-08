from django.contrib import admin
from .models import EnvironmentalStats


@admin.register(EnvironmentalStats)
class EnvironmentalStatsAdmin(admin.ModelAdmin):
    list_display    = ('date', 'total_energy_generated', 'co2_saved', 'cost_saved', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering        = ('-date',)
