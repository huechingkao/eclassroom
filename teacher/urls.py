# -*- coding: utf8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('classroom/', views.ClassroomListView.as_view()),
    path('classroom/create/', views.ClassroomCreate.as_view()),    
    path('classroom/<int:pk>/update/', views.ClassroomUpdate.as_view()),  
]