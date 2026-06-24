from django.urls import path
from . import views

urlpatterns = [

    path('categories/', views.category_view, name='category_view'),
     path('create-material/', views.material_create_view, name='material_create'),
     path('materials_list/', views.material_list_view, name='material_list'),
     path('material-detail/<int:pk>/', views.material_detail_view, name='material_detail'),
     path('delete/<int:pk>/', views.material_delete_view, name='material_delete'),
      path('material-update/<int:pk>/', views.material_update_view, name='material_update'),
       path('stock-movements/', views.stock_movement_list_create, name='stock_movement_list'),
       # urls.py

path(
    "customer_materials/<int:pk>/",
    views.customer_material_detail_view,
    name="customer_material_detail",
),
        path('customer_materials/', views.customer_material_list_view, name='customer_material_list'),

]