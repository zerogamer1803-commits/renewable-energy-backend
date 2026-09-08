from django.db import models


class StreetLight(models.Model):
    STATUS_CHOICES = [
        ('Working',     'Working'),
        ('Non-Working', 'Non-Working'),
        ('Fault',       'Fault'),
        ('Offline',     'Offline'),
    ]
    STATE_CHOICES = [
        ('ON',  'ON'),
        ('OFF', 'OFF'),
    ]
    COMM_CHOICES = [
        ('Connected',    'Connected'),
        ('Disconnected', 'Disconnected'),
        ('Weak Signal',  'Weak Signal'),
    ]

    light_id             = models.CharField(max_length=20, unique=True, db_index=True)
    location             = models.CharField(max_length=100, db_index=True)
    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Working', db_index=True)
    state                = models.CharField(max_length=5,  choices=STATE_CHOICES,  default='OFF',    db_index=True)
    power                = models.FloatField(default=0.0,  help_text='Power consumption in W')
    voltage              = models.FloatField(default=0.0,  help_text='Voltage in V')
    fault                = models.CharField(max_length=100, default='None', blank=True)
    communication_status = models.CharField(max_length=20, choices=COMM_CHOICES, default='Connected')
    brightness           = models.FloatField(default=100.0, help_text='Brightness 0–100 %')
    last_updated         = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Street Light'
        verbose_name_plural = 'Street Lights'
        ordering            = ['light_id']

    def __str__(self):
        return f'{self.light_id} — {self.location} ({self.status} / {self.state})'


class StreetLightHistory(models.Model):
    STATE_CHOICES = [
        ('ON',  'ON'),
        ('OFF', 'OFF'),
    ]

    street_light = models.ForeignKey(StreetLight, on_delete=models.CASCADE, related_name='history')
    state        = models.CharField(max_length=5, choices=STATE_CHOICES)
    power        = models.FloatField(default=0.0, help_text='Power in W at this point in time')
    timestamp    = models.DateTimeField(db_index=True)

    class Meta:
        verbose_name        = 'Street Light History Record'
        verbose_name_plural = 'Street Light History'
        ordering            = ['-timestamp']

    def __str__(self):
        return f'{self.street_light.light_id} | {self.timestamp:%Y-%m-%d %H:%M} | {self.state}'


class Fault(models.Model):
    FAULT_TYPE_CHOICES = [
        ('LED Failure',           'LED Failure'),
        ('Power Failure',         'Power Failure'),
        ('Communication Failure', 'Communication Failure'),
        ('Voltage Issue',         'Voltage Issue'),
        ('Other',                 'Other'),
    ]
    SEVERITY_CHOICES = [
        ('Critical', 'Critical'),
        ('Warning',  'Warning'),
        ('Info',     'Info'),
    ]

    street_light = models.ForeignKey(StreetLight, on_delete=models.CASCADE, related_name='faults')
    fault_type   = models.CharField(max_length=30, choices=FAULT_TYPE_CHOICES, db_index=True)
    severity     = models.CharField(max_length=10, choices=SEVERITY_CHOICES,   db_index=True)
    message      = models.TextField(blank=True, default='')
    resolved     = models.BooleanField(default=False, db_index=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    resolved_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Fault'
        verbose_name_plural = 'Faults'
        ordering            = ['-created_at']

    def __str__(self):
        status = 'Resolved' if self.resolved else 'Active'
        return f'{self.street_light.light_id} — {self.fault_type} [{self.severity}] ({status})'
