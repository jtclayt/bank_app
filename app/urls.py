from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/1', views.accountDetails),
    path('purchase', views.purchase),
    path('transfer', views.transfer),
    path('bill', views.bill),
    path('external-transfer/1', views.extTransfer),
    path('external-transfer', views.extContacts),
    path('atm', views.atm),
]
