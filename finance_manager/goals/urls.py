from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.goal_list, name='goal_list'),
    path('goals/new/', views.goal_create, name='goal_create'),
    path('goals/edit/<int:id>/', views.goal_edit, name='goal_edit'),
]
