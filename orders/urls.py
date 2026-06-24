# orders/urls.py

from django.urls import path
from . import views

urlpatterns = [

    # Product order page (Amazon-style checkout)
    path(
        'order/<int:material_id>/',
        views.customer_create_order,
        name='customer_create_order'
    ),
    path("driver/orders/on-route/", views.driver_on_route_orders, name="driver_on_route_orders"),

    path("order/success/<int:order_id>/", views.order_success_view, name="order_success"),
    path("my-orders/", views.customer_orders, name="customer_orders"),
    path("admin/orders/pending/", views.admin_pending_orders, name="admin_pending_orders"),
    path("admin/orders/assigned/", views.admin_assigned_orders, name="admin_assigned_orders"),
    path("admin/orders/on-route/", views.admin_on_route_orders, name="admin_on_route_orders"),
    path(
        "orders/<int:pk>/delete/",
        views.order_delete,
        name="order_delete"
    ),

    path("admin_orders/<int:pk>/", views.admin_order_detail, name="admin_order_detail"),
    path("admin/orders/delivered/", views.admin_delivered_orders, name="admin_delivered_orders"),
    path('driver/orders/assigned/', views.driver_assigned_orders, name='driver_assigned_orders'),
    path('driver/order/<int:pk>/', views.driver_order_detail, name='driver_order_detail'),
    path('driver/order/<int:pk>/status/<str:status>/', views.update_order_status, name='update_order_status'),
    path("driver/orders/delivered/", views.driver_delivered_orders, name="driver_delivered_orders"),
]
