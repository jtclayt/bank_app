from django.urls import path
from .views import index, LoginView, RegisterView, EditUserView, logout
from .views import change_password

app_name = 'users'

urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditUserView.as_view(), name='edit'),
    path('edit/password/', change_password, name='change_password'),
    path('logout/', logout, name='logout')
]
