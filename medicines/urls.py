from django.urls import path
from . import views

urlpatterns = [

    path('novo/', views.new_medicine, name='new_medicine'),
    path('<int:id>/', views.details_medicine, name='details_medicine'),
    path('editar/<int:id>/', views.update_medicine, name='update_medicine'),
    path('deletar/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('', views.all_medicine, name='all_medicine'),
]
