from django.urls import path
from . import views

urlpatterns = [
    path('', views.savings_list, name='savings_list'),  # List of savings goals
    path('create/', views.savings_create, name='savings_create'),  # Create a new saving goal
    path('<int:pk>/edit/', views.savings_edit, name='savings_edit'),  # Edit a saving goal
    path('<int:pk>/delete/', views.savings_delete, name='savings_delete'),  # Delete a saving goal
]
