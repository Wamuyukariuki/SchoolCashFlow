from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from budget import views as budget_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('budget/', include('budget.urls')),  # Include the budget app URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', budget_views.dashboard, name='dashboard'),
    path('signup/', budget_views.signup, name='signup'),
    path('savings/', include('savings.urls')),
    path('debt/', include('debt.urls')),
    path('goals/', include('goals.urls')),
]
