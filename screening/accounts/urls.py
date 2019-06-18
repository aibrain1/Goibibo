from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='accounts'),
    path('logout', views.logout, name='logout'),
    path('loginUser', views.loginAccount, name='loginUser'),
    path('register', views.registerView, name='register'),
 	path('registerUser', views.registerNewUser, name='registerUser'),
 	path('dashboard', include('dashboard.urls'))
]
