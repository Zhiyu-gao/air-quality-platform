from django.db import models

# Create your models here.
class AirQualityHealthDataset(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    aqi = models.CharField(max_length=255, blank=True, null=True)
    pm2_5 = models.CharField(max_length=255, blank=True, null=True)
    pm10 = models.CharField(max_length=255, blank=True, null=True)
    no2 = models.CharField(max_length=255, blank=True, null=True)
    o3 = models.CharField(max_length=255, blank=True, null=True)
    temperature = models.CharField(max_length=255, blank=True, null=True)
    humidity = models.CharField(max_length=255, blank=True, null=True)
    hospital_admissions = models.CharField(max_length=255, blank=True, null=True)
    population_density = models.CharField(max_length=255, blank=True, null=True)
    hospital_capacity = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'air_quality_health_dataset'