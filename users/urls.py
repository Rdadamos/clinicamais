from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'', auth_views.LoginView.as_view(template_name="users/login.html"), name='login')
]
