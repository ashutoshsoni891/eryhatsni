from django.db.models import fields
from rest_framework import serializers
from django.conf import settings

from . import models

class globalDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.globalDB
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['profile'] = profileSerializer(models.Profile.objects.filter(globaldb=instance), many=True).data
        return data

class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'