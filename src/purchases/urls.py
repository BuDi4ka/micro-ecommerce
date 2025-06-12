from django.urls import path

from . import views

app_name = "purchases"

urlpatterns = [
    path("start/", views.purchase_start, name="start"),
    path("success/", views.purchase_success, name="success"),
    path("stopped/", views.purchase_stopped, name="stopped"),
]
