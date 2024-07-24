from rest_framework import serializers

from .models import ResumeData


class ResumeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = '__all__'
