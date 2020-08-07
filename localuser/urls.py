from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit/', views.edit_view, name='edit'),
    path('people', views.people_view, name='people'),
    path('user_detail/<int:pk>/<str:username>', views.user_detail_view, name='user_detail'),
    path('follow/', views.follow_view, name='follow'),
]