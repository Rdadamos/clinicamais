from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('consultas/<int:id_patient>/', views.appointments, name='appointments'),
    path('nova_consulta/<int:id_patient>/', views.new_appointment_doctor, name='new_appointment_doctor'),
    path('nova_consulta/<int:id_patient>/<int:id_doctor>/', views.new_appointment, name='new_appointment'),
    path('consulta/cancelar/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path('agenda/<int:id>/', views.doctor_schedule, name='doctor_schedule'),
]
