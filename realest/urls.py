from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.index , name="index"),
    path('agent/<str:clas>', views.post , name="post"),
    path('onland', views.land , name="land"),
    path('delete/<int:id>', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('login', views.Login, name='login' ),
    path('logout', views.Logout_request, name='logout' ),
    path('register', views.register, name='register'),
    path('', views.public, name='public'),
    

]
