# -*- coding: utf8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('classroom/', views.ClassroomList.as_view()),
    path('classroom/create/', views.ClassroomCreate.as_view()),    
    path('classroom/<int:pk>/update/', views.ClassroomUpdate.as_view()),  
    path('announce/<int:classroom_id>/create/', views.AnnounceCreate.as_view()),      
    path('assignment/<int:classroom_id>/', views.AssignmentList.as_view()),  
    path('assignment/<int:classroom_id>/create/', views.AssignmentCreate.as_view()), 
    path('assignment/scoring/<int:assignment_id>/', views.ScoreList.as_view()),  
    path('assignment/scoring/<int:assignment_id>/<int:pk>/update/', views.ScoreUpdate.as_view()),   
]