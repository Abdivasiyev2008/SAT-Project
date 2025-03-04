# serializers.py
from rest_framework import serializers
from .models import LeakPassword
from rest_framework import serializers

class LeakCountSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()

class SearchURLSerializer(serializers.Serializer):
    search_text = serializers.CharField(max_length=255)

class LeakPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeakPassword
        fields = '__all__'  # Barcha maydonlarni olish
