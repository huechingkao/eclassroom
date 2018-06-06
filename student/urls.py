# -*- coding: utf8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('classroom/', views.ClassroomList.as_view()),
    path('classroom/join/', views.ClassroomJoinList.as_view()),    
    path('classroom/<int:pk>/enroll/', views.ClassroomEnrollCreate.as_view()), 
    path('classroom/<int:pk>/classmate/', views.ClassmateList.as_view()),    
    path('classroom/<int:pk>/seat/', views.ClassroomSeatUpdate.as_view()),   
    path('assignment/<int:classroom_id>/', views.AssignmentList.as_view()),   
    path('assignment/<int:assignment_id>/create/', views.AssignmentCreate.as_view()),
    path('assignment/work/<int:pk>/update', views.AssignmentUpdate.as_view()),
    path('assignment/memo/<int:classroom_id>/<int:assignment_id>/', views.MemoList.as_view()),     
    path('questionary/result/<int:classroom_id>/', views.QuestionaryView.as_view()),  
]