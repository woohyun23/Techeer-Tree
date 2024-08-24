from django.urls import path, include
from rest_framework import routers
from wishes.views import wishViewSet

router = routers.DefaultRouter()
router.register(r'wishes', wishViewSet)

urlpatterns = [
    path('',include(router.urls)),
]