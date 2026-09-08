from django.db import models


class Energy(models.Model):
    SOURCE_CHOICES = [
        ('Solar',    'Solar'),
        ('Footstep', 'Footstep'),
    ]

    source       = models.CharField(max_length=20, choices=SOURCE_CHOICES, unique=True, db_index=True)
    power_output = models.FloatField(default=0.0,  help_text='Current power output in kW')
    energy_today = models.FloatField(default=0.0,  help_text='Energy generated today in kWh')
    energy_week  = models.FloatField(default=0.0,  help_text='Energy generated this week in kWh')
    energy_month = models.FloatField(default=0.0,  help_text='Energy generated this month in kWh')
    efficiency   = models.FloatField(default=0.0,  help_text='Efficiency percentage 0–100')
    peak_power   = models.FloatField(default=0.0,  help_text='Peak power recorded today in kW')
    timestamp    = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Energy Source'
        verbose_name_plural = 'Energy Sources'
        ordering            = ['source']

    def __str__(self):
        return f'{self.source} — {self.power_output} kW'


class EnergyHistory(models.Model):
    SOURCE_CHOICES = [
        ('Solar',    'Solar'),
        ('Footstep', 'Footstep'),
        ('Total',    'Total'),
    ]

    source    = models.CharField(max_length=20, choices=SOURCE_CHOICES, db_index=True)
    energy    = models.FloatField(default=0.0, help_text='Energy in kWh')
    date      = models.DateField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Energy History Record'
        verbose_name_plural = 'Energy History'
        ordering            = ['-date', 'source']
        unique_together     = ('source', 'date')

    def __str__(self):
        return f'{self.source} | {self.date} | {self.energy} kWh'
