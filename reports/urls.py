from django.urls import path
from . import views 

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
     path('admin_customer_list', views.admin_customer_list, name='admin_customer_list'),
     path('admin_customer_details/<int:pk>/', views.admin_customer_detail, name='admin_customer_detail'),

]