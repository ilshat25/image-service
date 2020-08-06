from django.urls import path

from . import views

app_name = "images"

urlpatterns = [
    path('detail/<int:pk>/<slug:slug>/', views.detail_view, name="detail"),
    path('add/', views.add_view, name="add"),
    path('all/', views.all_view, name="all"),
]