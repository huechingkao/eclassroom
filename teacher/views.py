from django.shortcuts import render
from teacher.models import Classroom, Assignment
from student.models import Enroll
from django.views import generic
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from account.models import Message, MessagePoll
from account.forms import LineForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response, redirect
from student.models import Work
from teacher.forms import ScoreForm
from django.urls import reverse

class ClassroomList(generic.ListView):
    model = Classroom
    ordering = ['-id']
    paginate_by = 3   
    
class ClassroomCreate(CreateView):
    model =Classroom
    fields = ["name", "password"]
    success_url = "/teacher/classroom"   
    template_name = 'form.html'
      
    def form_valid(self, form):
        valid = super(ClassroomCreate, self).form_valid(form)
        classroom = form.save(commit=False)
        classroom.teacher_id = self.request.user.id
        classroom.save() 
        enroll = Enroll(classroom_id=classroom.id, student_id=classroom.teacher_id, seat=0)
        enroll.save()
        return valid
    
class ClassroomUpdate(UpdateView):
    model = Classroom
    fields = ["name", "password"]
    success_url = "/teacher/classroom"   
    template_name = 'form.html'
    
#新增一個公告
class AnnounceCreate(LoginRequiredMixin, CreateView):
    model = Message
    form_class = LineForm
    success_url = '/account/dashboard'    
    template_name = 'teacher/announce_form.html'     

    def form_valid(self, form):
        valid = super(AnnounceCreate, self).form_valid(form)
        self.object = form.save(commit=False)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        self.object.title = u"[公告]" + classroom.name + ":" + self.object.title
        self.object.author_id = self.request.user.id
        self.object.save()
        # 訊息
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id'])
        for enroll in enrolls :
            messagepoll = MessagePoll(message_id=self.object.id, reader_id=enroll.student_id)
            messagepoll.save()              
        return valid
      
    # 限本班教師
    def render_to_response(self, context):
        teacher_id = Classroom.objects.get(id=self.kwargs['classroom_id']).teacher_id
        if not teacher_id == self.request.user.id:
            return redirect('/')
        return super(AnnounceCreate, self).render_to_response(context)       
      
    def get_context_data(self, **kwargs):
        context = super(AnnounceCreate, self).get_context_data(**kwargs)
        context['classroom'] = Classroom.objects.get(id=self.kwargs['classroom_id'])
        return context
      
class AssignmentList(generic.ListView):
    model = Assignment
    template_name = "teacher/assignment_list.html"
    ordering = ['-id']   
    
    # 限本班教師
    def render_to_response(self, context):
        teacher_id = Classroom.objects.get(id=self.kwargs['classroom_id']).teacher_id
        if not teacher_id == self.request.user.id:
            return redirect('/')
        return super(AssignmentList, self).render_to_response(context)   
      
    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context      
      
class AssignmentCreate(CreateView):
    model =Assignment
    fields = ["title"]
    success_url = "/teacher/assignment"   
    template_name = 'form.html'
      
    def form_valid(self, form):
        valid = super(AssignmentCreate, self).form_valid(form)
        assignment = form.save(commit=False)
        assignment.classroom_id = self.kwargs['classroom_id']
        assignment.save() 
        return redirect("/teacher/assignment/"+str(self.kwargs['classroom_id'])) 

class ScoreList(generic.ListView):
    model = Work
    template_name = "teacher/score_list.html"

    def get_context_data(self, **kwargs):
        context = super(ScoreList, self).get_context_data(**kwargs)
        assignment = Assignment.objects.get(id=self.kwargs['assignment_id'])
        enrolls = Enroll.objects.filter(classroom_id=assignment.classroom_id).order_by("seat")
        student_ids = list(map(lambda a: a.student_id, enrolls))
        works = Work.objects.filter(assignment_id=self.kwargs['assignment_id'], student_id__in=student_ids)
        work_dict = dict((f.student_id, f) for f in works)
        scores = []
        for enroll in enrolls:
            if enroll.student_id in work_dict:
                scores.append([enroll, work_dict[enroll.student_id]])
            else :
                scores.append([enroll, None])
        context['scores'] = scores
        context['assignment_id'] = self.kwargs['assignment_id']
        return context
      
class ScoreUpdate(UpdateView):
    model = Work
    form_class = ScoreForm
    template_name = "teacher/score_form.html"      
    
    def get_success_url(self):       
        return "/teacher/assignment/scoring/" + str(self.kwargs['assignment_id'])
      
    def get_context_data(self, **kwargs):
        context = super(ScoreUpdate, self).get_context_data(**kwargs)
        context['work'] = Work.objects.get(id=self.kwargs["pk"])
        return context      