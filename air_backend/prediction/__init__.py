# Django模型类型存根
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import Manager
    
    class AirQualityHealthDataset:
        objects: Manager
        city: str
        date: str
        aqi: str
        pm2_5: str
        pm10: str
        no2: str
        o3: str
        temperature: str
        humidity: str
        hospital_admissions: str
        population_density: str
        hospital_capacity: str
