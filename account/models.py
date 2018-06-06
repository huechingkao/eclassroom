# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# 訊息
class Message(models.Model):
    author_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    typing = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    title = models.CharField(max_length=250)
    content = models.TextField(default='')
    url = models.CharField(max_length=250)
    publication_date = models.DateTimeField(auto_now_add=True)
			
# 訊息附件
class MessageContent(models.Model):
    message_id =  models.IntegerField(default=0)
    author_id = models.IntegerField(default=0)
    title =  models.CharField(max_length=250,null=True,blank=True)
    filename = models.CharField(max_length=250,null=True,blank=True)    
    publication_date = models.DateTimeField(auto_now_add=True)

# 訊息池    
class MessagePoll(models.Model):
    message_type = models.IntegerField(default=0)
    message_id = models.IntegerField(default=0)
    reader_id = models.IntegerField(default=0)
    classroom_id = models.IntegerField(default=0)
    read = models.BooleanField(default=False)
    
    @property
    def message(self):
        return Message.objects.get(id=self.message_id)
      
# 個人檔案資料
class Profile(models.Model):
	    user = models.OneToOneField(User, on_delete=models.CASCADE)
    	# 積分
	    point = models.IntegerField(default=0)
      
# 積分記錄 
class PointHistory(models.Model):
    # 使用者序號
	  user_id = models.IntegerField(default=0)
  	# 積分項目
	  message = models.CharField(max_length=100)
	  # 記載時間 
	  publication_date = models.DateTimeField(auto_now_add=True)

#問卷
class Questionary(models.Model):
    user_id = models.IntegerField(default=0)
    q1 = models.IntegerField(default=0)
    q2 = models.IntegerField(default=0)
    q3 = models.IntegerField(default=0)
    t1 = models.TextField(default='')    
    t2 = models.TextField(default='')