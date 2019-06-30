from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url('atendente/', views.attendant, name='attendant'),
    url('logout/', auth_views.logout_then_login, {'login_url': '/'}, name='logout'),
    url('', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
]
