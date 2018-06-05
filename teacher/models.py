# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

# 班級
class Classroom(models.Model):
    # 班級名稱
    name = models.CharField(max_length=30, verbose_name='班級名稱')
    # 選課密碼
    password = models.CharField(max_length=30, verbose_name='選課密碼')
    # 授課教師
    teacher_id = models.IntegerField(default=0)
    
    @property
    def teacher(self):
        return User.objects.get(id=self.teacher_id)  
        
#作業
class Assignment(models.Model):
    title = models.CharField(max_length=250, verbose_name='作業名稱')    
    classroom_id = models.IntegerField(default=0)
    publication_date = models.DateTimeField(auto_now_add=True)
