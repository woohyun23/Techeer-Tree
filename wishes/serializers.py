from rest_framework import serializers
from .models import wish

class wishSerializer(serializers.ModelSerializer):
    class Meta:
        model = wish
        fields = ['id', 'title', 'content', 'created_at']