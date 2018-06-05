# -*- coding: UTF-8 -*-
from django import forms
from student.models import Enroll, Work

class ScoreForm(forms.ModelForm): 
    CHOICES = (
            (100, "你好棒(100分)"),
            (90, "90分"),
            (80, "80分"),
            (70, "70分"),
            (60, "60分"),
    )
   
    score = forms.ChoiceField(choices = CHOICES, required=True, label="分數")

    class Meta:
        model = Work
        fields = ('score',)
        
