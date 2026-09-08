from django.db import models


class Battery(models.Model):
    STATUS_CHOICES = [
        ('Charging',    'Charging'),
        ('Discharging', 'Discharging'),
        ('Full',        'Full'),
        ('Idle',        'Idle'),
        ('Fault',       'Fault'),
    ]

    battery_id            = models.CharField(max_length=20, unique=True, db_index=True)
    capacity              = models.FloatField(default=0.0,  help_text='Total capacity in kWh')
    stored_energy         = models.FloatField(default=0.0,  help_text='Currently stored energy in kWh')
    battery_level         = models.FloatField(default=0.0,  help_text='Battery level 0–100 %')
    voltage               = models.FloatField(default=0.0,  help_text='Voltage in V')
    current               = models.FloatField(default=0.0,  help_text='Current in A')
    temperature           = models.FloatField(default=0.0,  help_text='Temperature in °C')
    health                = models.FloatField(default=100.0, help_text='Battery health 0–100 %')
    status                = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Idle', db_index=True)
    charging_power        = models.FloatField(default=0.0,  help_text='Charging power in kW')
    energy_received_today = models.FloatField(default=0.0,  help_text='kWh received today')
    energy_supplied_today = models.FloatField(default=0.0,  help_text='kWh supplied today')
    charge_cycles         = models.PositiveIntegerField(default=0)
    last_full_charge      = models.DateTimeField(null=True, blank=True)
    timestamp             = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Battery'
        verbose_name_plural = 'Batteries'
        ordering            = ['battery_id']

    def __str__(self):
        return f'{self.battery_id} — {self.battery_level}% ({self.status})'


class BatteryHistory(models.Model):
    battery       = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='history')
    battery_level = models.FloatField(help_text='Battery level % at this point in time')
    temperature   = models.FloatField(help_text='Temperature °C at this point in time')
    timestamp     = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name        = 'Battery History Record'
        verbose_name_plural = 'Battery History'
        ordering            = ['-timestamp']

    def __str__(self):
        return f'{self.battery.battery_id} | {self.timestamp:%Y-%m-%d %H:%M} | {self.battery_level}%'
