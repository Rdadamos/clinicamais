from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('agenda/<int:id>/', views.doctor_schedule, name='doctor_schedule'),
]
