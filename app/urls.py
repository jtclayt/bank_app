from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.index),
    path('accounts/1', views.accountDetails),
    path('purchase', views.purchase),
    path('transfer', views.transfer),
]
