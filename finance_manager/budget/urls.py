from django.urls import path
from . import views

urlpatterns = [
    path('expenses/', views.expense_list, name='expense_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expenses/create/', views.expense_create, name='expense_create'),
]
