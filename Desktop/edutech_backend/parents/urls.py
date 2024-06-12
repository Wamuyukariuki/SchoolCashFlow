from django.urls import path, include
from rest_framework.routers import DefaultRouter
from parents.views import ParentViewSet

router = DefaultRouter()
router.register(r'parents', ParentViewSet, basename='parent')

urlpatterns = [
    path('', include(router.urls)),
]