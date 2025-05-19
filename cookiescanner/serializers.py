from rest_framework import serializers
from .models import CookieData

class CookieDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookieData
        fields = '__all__'
