from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "stock_predict"

urlpatterns = [
    path("home/",views.home,name='home'),
    path("predict/",views.predict_stock_action,name='predict'),
]
