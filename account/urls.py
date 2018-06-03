# -*- coding: utf8 -*-
from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="dashboard.html")),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),  
    path('user/', views.UserListView.as_view()),
    path('user/create/', views.UserCreate.as_view()),    
    path('user/<int:pk>', views.UserDetailView.as_view()),
    path('user/<int:pk>/update/', views.UserUpdate.as_view()), 
    path('user/<int:pk>/password/', views.UserPasswordUpdate.as_view()),
    path('user/<int:pk>/teacher/', views.UserTeacherView.as_view()),    
    #註冊帳號
    #path('user/create/', views.UserCreate.as_view()),
 ]