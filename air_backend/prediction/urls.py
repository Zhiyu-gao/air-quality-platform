from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirQualityViewSet

router = DefaultRouter()
router.register(r'prediction', AirQualityViewSet)

urlpatterns = [
    path('', include(router.urls))
]
