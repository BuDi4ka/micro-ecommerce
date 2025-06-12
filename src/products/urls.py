from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('<slug:handle>/', views.product_detail, name='detail'),
    path('<slug:handle>/download/<int:pk>/', views.product_attacment_download, name='attachment-download'),
]
