from django.shortcuts import render
from rest_framework import viewsets
from .models import wish
from .serializers import wishSerializer

class wishViewSet(viewsets.ModelViewSet):
    queryset = wish.objects.all().order_by('-created_at')
    serializer_class = wishSerializer

    # wish 생성 시 보류를 기본 값으로 설정 -> models에서 pending으로 설정했는데 여기서 또 설정??
    def perform_create(self, serializer):
        serializer.save(is_confirm='pending')
