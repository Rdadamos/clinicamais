from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url('atendente/novo/', views.new_attendant, name='new_attendant'),
    path('atendente/<int:id>/', views.details_attendant, name='details_attendant'),
    path('atendente/editar/<int:id>/', views.update_attendant, name='update_attendant'),
    path('atendente/deletar/<int:id>/', views.delete_attendant, name='delete_attendant'),
    url('atendente/', views.all_attendant, name='all_attendant'),
    url('logout/', auth_views.logout_then_login, {'login_url': '/'}, name='logout'),
    url('', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
]
