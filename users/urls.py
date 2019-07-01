from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .decorators import anonimous_only

urlpatterns = [
    url('atendente/novo/', views.new_attendant, name='new_attendant'),
    path('atendente/<int:id>/', views.details_attendant, name='details_attendant'),
    path('atendente/editar/<int:id>/', views.update_attendant, name='update_attendant'),
    path('atendente/deletar/<int:id>/', views.delete_attendant, name='delete_attendant'),
    url('atendente/', views.all_attendant, name='all_attendant'),

    url('medico/novo/', views.new_doctor, name='new_doctor'),
    path('medico/<int:id>/', views.details_doctor, name='details_doctor'),
    path('medico/editar/<int:id>/', views.update_doctor, name='update_doctor'),
    path('medico/deletar/<int:id>/', views.delete_doctor, name='delete_doctor'),
    url('medico/', views.all_doctor, name='all_doctor'),

    url('paciente/novo/', views.new_patient, name='new_patient'),
    path('paciente/<int:id>/', views.details_patient, name='details_patient'),
    path('paciente/editar/<int:id>/', views.update_patient, name='update_patient'),
    path('paciente/deletar/<int:id>/', views.delete_patient, name='delete_patient'),
    url('paciente/', views.all_patient, name='all_patient'),

    url('logout/', auth_views.logout_then_login, {'login_url': '/'}, name='logout'),
    path('', anonimous_only(auth_views.LoginView.as_view(template_name="users/login.html")), name='login'),
]
