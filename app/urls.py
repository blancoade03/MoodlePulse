from django.urls import include, re_path
from rest_framework import routers
from app.viewsets import userviewset


router = routers.DefaultRouter()

router.register(r'user', userviewset, basename='usuario')

urlpatterns = [
    re_path('', include(router.urls)),
]
