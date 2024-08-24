from django.shortcuts import render
from rest_framework import viewsets
from .models import wish
from .serializers import wishSerializer

class wishViewSet(viewsets.ModelViewSet):
    queryset = wish.objects.all().order_by('-created_at')
    serializer_class = wishSerializer