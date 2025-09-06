from django.contrib import admin
from .models import AirQualityHealthDataset

@admin.register(AirQualityHealthDataset)
class AirQualityHealthDatasetAdmin(admin.ModelAdmin):
    list_display = ['city', 'date', 'aqi', 'pm2_5', 'pm10', 'no2', 'o3', 'temperature', 'humidity', 'hospital_admissions']
    list_filter = ['city', 'date']
    search_fields = ['city', 'date']
    readonly_fields = ['id']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('city', 'date')
        }),
        ('空气质量指标', {
            'fields': ('aqi', 'pm2_5', 'pm10', 'no2', 'o3')
        }),
        ('环境条件', {
            'fields': ('temperature', 'humidity')
        }),
        ('医疗相关', {
            'fields': ('hospital_admissions', 'population_density', 'hospital_capacity')
        }),
    )
