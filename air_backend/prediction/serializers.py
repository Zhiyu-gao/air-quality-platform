from rest_framework import serializers
from .models import AirQualityHealthDataset

class AirQualityHealthDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityHealthDataset
        fields = '__all__'