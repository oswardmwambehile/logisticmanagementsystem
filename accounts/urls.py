from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(
        'register/',
        views.register_view,
        name='register'
    ),

     path('logout',views.logout_user, name='logout'),
     path("login/", views.login_view, name="login"),
     path('profile/', views.driver_profile, name='driver_profile'),
      path('change-password/', views.change_password, name='change_password'),
       path('customer_change_password/', views.customer_change_password, name='customer_change_password'),

     
      path("driver_dashboard/", views.driver_dashboard, name="driver_dashboard"),
       path(
        "drivers/create/",
        views.driver_create,
        name="driver_create"
    ),
    path(
    "drivers/",
    views.driver_list,
    name="driver_list"
),
path(
    "drivers/<int:pk>/",
    views.driver_detail,
    name="driver_detail"
),

path(
    "drivers/<int:pk>/update/",
    views.driver_update,
    name="driver_update"
),

path(
    "drivers/delete/<int:pk>/",
    views.driver_delete,
    name="driver_delete"
),

]