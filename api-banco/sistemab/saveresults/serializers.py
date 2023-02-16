from rest_framework import serializers
from saveresults import models


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Detections
        fields = '__all__'
