# -*- coding: UTF-8 -*-
from django import forms
from django.contrib.auth.models import User, Group
from account.models import Message, MessagePoll, MessageContent
from account.models import Questionary

class UserRegistrationForm(forms.ModelForm): 
    error_messages = {
        'duplicate_username': ("此帳號已被使用")
    }
    
    username = forms.RegexField(
        label="User name", max_length=30, regex=r"^[\w.@+-]+$",
        error_messages={
            'invalid': ("帳號名稱無效")
        }
    )
    
    password = forms.CharField(label='Password', 
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', 
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
            
    def clean_username(self):
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "帳號"
        self.fields['first_name'].label = "真實姓名"
        self.fields['last_name'].label = "學校名稱"
        self.fields['email'].label = "電子郵件"
        self.fields['password'].label = "密碼"
        self.fields['password2'].label = "再次確認密碼"    
        
class UserUpdateForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "帳號"
        self.fields['first_name'].label = "真實姓名"
        self.fields['last_name'].label = "學校名稱"
        self.fields['email'].label = "電子郵件"         

class UserPasswordForm(forms.ModelForm): 
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('password',)
        
    def __init__(self, *args, **kwargs):
        super(UserPasswordForm, self).__init__(*args, **kwargs)  
        self.fields['password'].label = "密碼"
  
class UserTeacherForm(forms.Form):    
    teacher = forms.BooleanField(required=False)
       
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('pk', None)
        super(UserTeacherForm, self).__init__(*args, **kwargs)  
        self.fields['teacher'].label = "教師"  
        self.fields['teacher'].initial = User.objects.get(id=user_id).groups.filter(name='teacher').exists()

# 新增一個私訊表單
class LineForm(forms.ModelForm):
    class Meta:
       model = Message
       fields = ['title','content',]
       
    def __init__(self, *args, **kwargs):
        super(LineForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "主旨"
        self.fields['title'].widget.attrs['size'] = 50
        self.fields['content'].label = "內容"
        self.fields['content'].required = False            
        self.fields['content'].widget.attrs['cols'] = 50
        self.fields['content'].widget.attrs['rows'] = 20          

# 新增一個問卷表單
class QuestionaryForm(forms.ModelForm):
    CHOICES=[(4,'非常同意'),
             (3,'同意'),
             (2,'不同意'),
             (1,'非常不同意')]  
    
    q1 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())   
    q2 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())   
    q3 = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())       
    
    class Meta:
        model = Questionary
        fields = ['q1','q2', 'q3', 't1', 't2']
        
    def __init__(self, *args, **kwargs):
        super(QuestionaryForm, self).__init__(*args, **kwargs)         
        self.fields['t1'].widget.attrs['cols'] = 80
        self.fields['t1'].widget.attrs['rows'] = 5         
        self.fields['t2'].widget.attrs['cols'] = 80
        self.fields['t2'].widget.attrs['rows'] = 5           

      