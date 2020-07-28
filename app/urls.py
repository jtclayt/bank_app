from django.urls import path
from .views import index, account_detail, AccountsView, PurchaseView, ATMView
from .views import TransferView, BillView, ContactsView, ExternalTransferView

app_name = 'app'

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', AccountsView.as_view(), name='accounts'),
    path('accounts/<int:account_id>/', account_detail, name='accounts_detail'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('bill/', BillView.as_view(), name='bill'),
    path('external-transfer/', ContactsView.as_view(), name='contacts'),
    path(
        'external-transfer/<int:contact_id>/',
        ExternalTransferView.as_view(),
        name='external_transfer'
    ),
    path('atm/', ATMView.as_view(), name='atm'),
]
