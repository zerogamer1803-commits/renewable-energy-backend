from django.core.management.base import BaseCommand
from django.utils import timezone

from energy.models import Energy, EnergyHistory
from battery.models import Battery, BatteryHistory
from streetlights.models import StreetLight, StreetLightHistory, Fault
from dashboard.models import EnvironmentalStats


class Command(BaseCommand):
    help = "Create sample data for the renewable energy dashboard"

    def handle(self, *args, **options):
        now = timezone.now()
        today = now.date()

        # ---------------------------------------------------------
        # ENERGY DATA
        # ---------------------------------------------------------
        solar, _ = Energy.objects.update_or_create(
            source="Solar",
            defaults={
                "power_output": 4.8,
                "energy_today": 16.3,
                "energy_week": 108.5,
                "energy_month": 421.7,
                "efficiency": 87.5,
                "peak_power": 6.2,
            },
        )

        footstep, _ = Energy.objects.update_or_create(
            source="Footstep",
            defaults={
                "power_output": 0.7,
                "energy_today": 2.4,
                "energy_week": 15.8,
                "energy_month": 62.4,
                "efficiency": 72.0,
                "peak_power": 1.1,
            },
        )

        # Energy history
        for source, values in {
            "Solar": [12.1, 14.5, 15.2, 13.8, 16.0, 17.1, 16.3],
            "Footstep": [1.5, 1.8, 2.0, 1.7, 2.2, 2.5, 2.4],
        }.items():
            for days_ago, value in enumerate(reversed(values)):
                date = today - timezone.timedelta(days=days_ago)

                EnergyHistory.objects.update_or_create(
                    source=source,
                    date=date,
                    defaults={
                        "energy": value,
                        "timestamp": now,
                    },
                )

        # ---------------------------------------------------------
        # BATTERY DATA
        # ---------------------------------------------------------
        battery, _ = Battery.objects.update_or_create(
            battery_id="BAT-001",
            defaults={
                "capacity": 25.0,
                "stored_energy": 19.5,
                "battery_level": 78.0,
                "voltage": 48.2,
                "current": 12.4,
                "temperature": 29.0,
                "health": 96.0,
                "status": "Charging",
                "charging_power": 2.8,
                "energy_received_today": 14.6,
                "energy_supplied_today": 9.3,
                "charge_cycles": 142,
                "last_full_charge": now,
            },
        )

        # Battery history
        for hours_ago, level, temperature in [
            (6, 61, 27.5),
            (5, 65, 28.0),
            (4, 69, 28.2),
            (3, 72, 28.5),
            (2, 75, 28.7),
            (1, 77, 28.9),
            (0, 78, 29.0),
        ]:
            BatteryHistory.objects.update_or_create(
                battery=battery,
                timestamp=now - timezone.timedelta(hours=hours_ago),
                defaults={
                    "battery_level": level,
                    "temperature": temperature,
                },
            )

        # ---------------------------------------------------------
        # STREET LIGHT DATA
        # ---------------------------------------------------------
        locations = [
            "Main Road",
            "College Road",
            "Market Area",
            "Bus Stand",
            "Railway Road",
            "Station Road",
            "Industrial Area",
            "Residential Area",
        ]

        # Create 120 lights
        for number in range(1, 121):
            if number <= 108:
                status = "Working"
            elif number <= 116:
                status = "Non-Working"
            else:
                status = "Fault"

            state = "ON" if number <= 96 else "OFF"

            if status == "Working":
                fault = "None"
                communication = "Connected"
            elif status == "Non-Working":
                fault = "Power Failure"
                communication = "Connected"
            else:
                fault = "LED Failure"
                communication = "Weak Signal"

            location = locations[(number - 1) % len(locations)]

            light, _ = StreetLight.objects.update_or_create(
                light_id=f"SL-{number:03d}",
                defaults={
                    "location": location,
                    "status": status,
                    "state": state,
                    "power": 80.0 if state == "ON" else 0.0,
                    "voltage": 230.0,
                    "fault": fault,
                    "communication_status": communication,
                    "brightness": 100.0 if state == "ON" else 0.0,
                },
            )

            StreetLightHistory.objects.create(
                street_light=light,
                state=state,
                power=80.0 if state == "ON" else 0.0,
                timestamp=now,
            )

        # ---------------------------------------------------------
        # FAULT DATA
        # ---------------------------------------------------------
        Fault.objects.all().delete()

        fault_lights = StreetLight.objects.filter(status__in=["Non-Working", "Fault"])

        for light in fault_lights:
            Fault.objects.create(
                street_light=light,
                fault_type="LED Failure"
                if light.status == "Fault"
                else "Power Failure",
                severity="Critical"
                if light.status == "Fault"
                else "Warning",
                message=f"{light.fault} detected on {light.light_id}",
                resolved=False,
            )

        # ---------------------------------------------------------
        # ENVIRONMENTAL / SAVINGS DATA
        # ---------------------------------------------------------
        EnvironmentalStats.objects.update_or_create(
            date=today,
            defaults={
                "total_energy_generated": 18.7,
                "co2_saved": 12.4,
                "cost_saved": 185.0,
                "timestamp": now,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Sample renewable energy dashboard data created successfully."
            )
        )