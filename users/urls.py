from django.urls import path
from .views import index, LoginView, RegisterView, EditUserView, logout

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditUserView.as_view(), name='edit'),
    path('logout/', logout, name='logout')
]
