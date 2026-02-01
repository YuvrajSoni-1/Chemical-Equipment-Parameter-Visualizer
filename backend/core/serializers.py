from rest_framework import serializers
from .models import DatasetWrapper, EquipmentData

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetWrapperSerializer(serializers.ModelSerializer):
    # We can include equipment data if needed, or keep it light
    class Meta:
        model = DatasetWrapper
        fields = ['id', 'filename', 'upload_date']
