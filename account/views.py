# -*- coding: utf8 -*-
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView
from .forms import UserRegistrationForm, UserUpdateForm, UserPasswordForm, UserTeacherForm, LineForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from student.models import Enroll
from account.models import Message, MessagePoll, MessageContent
from django.core.files.storage import FileSystemStorage
from uuid import uuid4
from django.core.exceptions import ObjectDoesNotExist

# 判斷是否為本班同學
def is_classmate(user_id, classroom_id):
    return Enroll.objects.filter(student_id=user_id, classroom_id=classroom_id).exists()

class SuperUserRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect("/account/login")
        return super(SuperUserRequiredMixin, self).dispatch(request,
            *args, **kwargs)

class LoginView(FormView):
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "login.html"

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if form.get_user().id == 1 and form.get_user().first_name == "":
            user = User.objects.get(id=1)
            user.first_name = "管理員"
            user.save()
          
        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(RedirectView):
    url = '/account/login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
      
class UserListView(SuperUserRequiredMixin, generic.ListView):
    model = User
    ordering = ['-id']
    paginate_by = 3   

class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    
class UserCreate(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = "/account/login"   
    template_name = 'form.html'
      
    def form_valid(self, form):
        valid = super(UserCreate, self).form_valid(form)
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.save()  
        return valid
    
class UserUpdate(SuperUserRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = "/account/user"   
    template_name = 'form.html'
    
class UserPasswordUpdate(SuperUserRequiredMixin, UpdateView):
    model = User
    form_class = UserPasswordForm
    success_url = "/account/user"   
    template_name = 'form.html'
    
    def form_valid(self, form):
        valid = super(UserPasswordUpdate, self).form_valid(form)
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data.get('password'))
        new_user.save()  
        return valid    

class UserTeacherView(SuperUserRequiredMixin, FormView):
    success_url = '/account/user'
    form_class = UserTeacherForm
    template_name = "form.html"
      
    def form_valid(self, form):
        valid = super(UserTeacherView, self).form_valid(form)
        user = User.objects.get(id=self.kwargs['pk'])
        try :
            group = Group.objects.get(name="teacher")	
        except ObjectDoesNotExist :
            group = Group(name="teacher")
            group.save()        
        if form.cleaned_data.get('teacher') :
            group.user_set.add(user)
        else: 
            group.user_set.remove(user)
        return valid  
      
    def get_form_kwargs(self):
        kwargs = super(UserTeacherView, self).get_form_kwargs()
        kwargs.update({'pk': self.kwargs['pk']})
        return kwargs

# 列出所有私訊
class LineListView(LoginRequiredMixin, generic.ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'account/line_list.html'    
    paginate_by = 20
    
    def get_queryset(self):     
        queryset = Message.objects.filter(author_id=self.request.user.id).order_by("-id")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LineListView, self).get_context_data(**kwargs)
        return context	 
        
# 列出同學以私訊
class LineClassmateListView(LoginRequiredMixin, generic.ListView):
    model = Enroll
    template_name = 'account/line_classmate.html'   
    
    def get_queryset(self):     
        queryset = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        return queryset
        
    # 限本班同學
    def render_to_response(self, context):
        if not is_classmate(self.request.user.id, self.kwargs['classroom_id']):
            return redirect('/')
        return super(LineClassmateListView, self).render_to_response(context)            
                
#新增一個私訊
class LineCreate(LoginRequiredMixin, CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.kwargs['user_id']
        self.object.typing = 2
        self.object.save()
        self.object.url = "/account/line/detail/" + str(self.kwargs['classroom_id']) + "/" + str(self.object.id)
        self.object.classroom_id = 0 - self.kwargs['classroom_id']
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/upload/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], message_type=2, classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()              
        return redirect("/account/dashboard")      
        
    def get_context_data(self, **kwargs):
        context = super(LineCreate, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
        
#回覆一個私訊
class LineReplyView(LoginRequiredMixin, CreateView):
    model = Message
    context_object_name = 'messages'    
    form_class = LineForm
    template_name = 'account/line_form_reply.html'     

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_name = User.objects.get(id=self.request.user.id).first_name
        self.object.title = u"[私訊]" + user_name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.reader_id = self.kwargs['user_id']
        self.object.typing = 2
        self.object.save()
        self.object.url = "/account/line/detail/" + str(self.kwargs['classroom_id']) + "/" + str(self.object.id)
        self.object.classroom_id = 0 - int(self.kwargs['classroom_id'])
        self.object.save()
        if self.request.FILES:
            for file in self.request.FILES.getlist('files'):
                content = MessageContent()
                fs = FileSystemStorage()
                filename = uuid4().hex
                content.title = file.name
                content.message_id = self.object.id
                content.filename = str(self.request.user.id)+"/"+filename
                fs.save("static/upload/"+str(self.request.user.id)+"/"+filename, file)
                content.save()
        # 訊息
        messagepoll = MessagePoll(message_id=self.object.id, reader_id=self.kwargs['user_id'], message_type=2, classroom_id=0-int(self.kwargs['classroom_id']))
        messagepoll.save()              
        return redirect("/account/line/")      
        
    def get_context_data(self, **kwargs):
        context = super(LineReplyView, self).get_context_data(**kwargs)
        context['user_id'] = self.kwargs['user_id']
        context['classroom_id'] = self.kwargs['classroom_id']
        message = Message.objects.get(id=self.kwargs['message_id'])
        title = "RE:" + message.title[message.title.find(":")+1:]
        context['title'] = title
        messagepolls = MessagePoll.objects.filter(reader_id=self.kwargs['user_id'],  classroom_id=0 - int(self.kwargs['classroom_id'])).order_by('-id')
        messages = []
        for messagepoll in messagepolls:
            message = Message.objects.get(id=messagepoll.message_id)
            if message.author_id == self.request.user.id :
                messages.append([message, messagepoll.read])
        context['messages'] = messages
        return context	 
    
# 訊息
class MessageListView(LoginRequiredMixin, generic.ListView):
    model = MessagePoll
    paginate_by = 20
    template_name = 'account/dashboard.html'
        
    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        queryset = []
        messagepolls = MessagePoll.objects.filter(reader_id=self.request.user.id).order_by('-message_id')
        for messagepoll in messagepolls:
            queryset.append([messagepoll, messagepoll.message])
        context['queryset'] = queryset        
        return context
      
class LineDetailView(generic.DetailView):
    model = Message
    template_name = "account/line_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(LineDetailView, self).get_context_data(**kwargs)
        context['files'] = MessageContent.objects.filter(message_id=self.kwargs['pk'])
        message = Message.objects.get(id=self.kwargs['pk'])
        context['messes'] = Message.objects.filter(author_id=message.author_id, reader_id=self.request.user.id).order_by("-id")
        try:
            if message.typing == 2:
                messagepoll = MessagePoll.objects.get(message_id=message.id)
            else:
                messagepoll = MessagePoll.objects.get(message_id=message.id, reader_id=self.request.user.id)
            if self.request.user.id == messagepoll.reader_id:
                messagepoll.read = True
            messagepoll.save()
        except :
            messagepoll = MessagePoll()        
        context['messagepoll'] = messagepoll
        return context    