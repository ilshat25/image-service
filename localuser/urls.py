from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit/', views.edit_view, name='edit'),
]