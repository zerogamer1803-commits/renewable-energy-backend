from django.db import models


class EnvironmentalStats(models.Model):
    total_energy_generated = models.FloatField(default=0.0, help_text='Total renewable energy generated in kWh')
    co2_saved              = models.FloatField(default=0.0, help_text='CO2 avoided in kg')
    cost_saved             = models.FloatField(default=0.0, help_text='Cost saved in local currency')
    date                   = models.DateField(unique=True, db_index=True)
    timestamp              = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Environmental Stats'
        verbose_name_plural = 'Environmental Stats'
        ordering            = ['-date']

    def __str__(self):
        return f'{self.date} — {self.total_energy_generated} kWh | CO2: {self.co2_saved} kg | Saved: {self.cost_saved}'
