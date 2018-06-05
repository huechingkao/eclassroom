# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from teacher.models import Classroom
from django.utils import timezone

# 學生選課資料
class Enroll(models.Model):
    # 學生序號
    student_id = models.IntegerField(default=0)
    # 班級序號
    classroom_id = models.IntegerField(default=0)
    # 座號
    seat = models.IntegerField(default=0)
	
    @property
    def classroom(self):
        return Classroom.objects.get(id=self.classroom_id)  

    @property        
    def student(self):
        return User.objects.get(id=self.student_id)      
    
#作業
class Work(models.Model):
    assignment_id = models.IntegerField(default=0)
    student_id = models.IntegerField(default=0)
    memo = models.TextField(default='', verbose_name='心得')
    file = models.FileField(blank=True,null=True, verbose_name='檔案', upload_to='work/')
    publication_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    
