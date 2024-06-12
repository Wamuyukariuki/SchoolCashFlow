from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserGroupView
router = DefaultRouter()
router.register(r'', UserGroupView, basename='')

urlpatterns = [
    path('', include(router.urls)),
]

