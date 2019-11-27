from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('consultas/<int:id>/', views.appointments, name='appointments'),
    path('nova_consulta/<int:id>/', views.new_appointment, name='new_appointment'),
    path('agenda/<int:id>/', views.doctor_schedule, name='doctor_schedule'),
]
