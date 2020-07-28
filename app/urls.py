from django.urls import path
from .views import index, AccountsView, AccountDetail

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('accounts', AccountsView.as_view(), name='accounts'),
    path('accounts/1', views.accountDetails),
    path('purchase', views.purchase),
    path('transfer', views.transfer),
    path('bill', views.bill),
    path('external-transfer/1', views.extTransfer),
    path('external-transfer', views.extContacts),
]
