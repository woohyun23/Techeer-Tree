from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from wishes.views import wishViewSet

router = DefaultRouter()
router.register(r'wishes', wishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]