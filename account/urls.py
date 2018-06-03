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
    path('line/classmate/<int:classroom_id>/', views.LineClassmateListView.as_view()),      
    path('line/<int:user_id>/<int:classroom_id>/create/', views.LineCreate.as_view()), 
    path('line/<int:pk>/', views.LineDetailView.as_view()),
    path('dashboard/',  views.MessageListView.as_view()),    
 ]