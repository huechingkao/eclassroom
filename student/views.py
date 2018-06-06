from django.shortcuts import render
from teacher.models import Classroom, Assignment
from student.models import Enroll, Work
from student.forms import EnrollForm
from django.views import generic
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import Profile, PointHistory
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from account.models import Questionary

# 判斷是否為本班同學
def is_classmate(user_id, classroom_id):
    return Enroll.objects.filter(student_id=user_id, classroom_id=classroom_id).exists()

class ClassroomList(generic.ListView):
    model = Classroom
    paginate_by = 3   
    template_name = 'student/classroom_list.html'
       
    def get_context_data(self, **kwargs):
        context = super(ClassroomList, self).get_context_data(**kwargs)
        queryset = []
        enrolls = Enroll.objects.filter(student_id=self.request.user.id)
        classroom_ids = list(map(lambda a: a.classroom_id, enrolls))        
        classroom_dict = dict((f.classroom_id, f) for f in enrolls)
        classrooms = Classroom.objects.filter(id__in=classroom_ids).order_by("-id")
        for classroom in classrooms:
            queryset.append([classroom, classroom_dict[classroom.id]])
        context['queryset'] = queryset 
        return context 

class ClassroomJoinList(generic.ListView):
    model = Classroom
    template_name = 'student/classroom_join.html'    
    
    def get_context_data(self, **kwargs):
        context = super(ClassroomJoinList, self).get_context_data(**kwargs)
        queryset = []
        enrolls = Enroll.objects.filter(student_id=self.request.user.id)
        classroom_ids = list(map(lambda a: a.classroom_id, enrolls))        
        classrooms = Classroom.objects.all().order_by("-id")
        for classroom in classrooms:
            if classroom.id in classroom_ids:
                queryset.append([classroom, True])
            else:
                queryset.append([classroom, False])
        context['queryset'] = queryset 
        return context 

class ClassroomEnrollCreate(CreateView):
    model = Enroll
    form_class = EnrollForm    
    success_url = "/student/classroom"  
    template_name = "form.html"
    
    def form_valid(self, form):
        valid = super(ClassroomEnrollCreate, self).form_valid(form)
        if form.cleaned_data['password'] == Classroom.objects.get(id=self.kwargs['pk']).password:
            enrolls = Enroll.objects.filter(student_id=self.request.user.id, classroom_id=self.kwargs['pk'])
            if not enrolls.exists():
                enroll = Enroll(student_id=self.request.user.id, classroom_id=self.kwargs['pk'], seat=form.cleaned_data['seat'])
                enroll.save()
        return valid

class ClassmateList(generic.ListView):
    model = Enroll   
    template_name = 'student/classmate.html'
    
    def get_queryset(self):
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['pk'])
        return enrolls  
      
class ClassroomSeatUpdate(UpdateView):
    model = Enroll
    fields = ['seat']
    success_url = "/student/classroom/"      
    template_name = "form.html"
    
class AssignmentList(generic.ListView):
    model = Assignment
    template_name = "student/assignment_list.html"
    
    def get_queryset(self):
        assignments = Assignment.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("-id")
        return assignments
      
    def get_context_data(self, **kwargs):
        context = super(AssignmentList, self).get_context_data(**kwargs)
        context['classroom_id'] = self.kwargs['classroom_id']
        return context      
      
class AssignmentCreate(CreateView):
    model = Work
    fields = ["memo", "file"]
    success_url = "/student/classroom"  
    template_name = "form.html"
    
    def form_valid(self, form):
        valid = super(AssignmentCreate, self).form_valid(form)
        work = form.save(commit=False)
        work.assignment_id = self.kwargs['assignment_id']
        work.student_id = self.request.user.id
        work.save()        
        profile = Profile.objects.get(user=self.request.user)
        profile.point = profile.point + 2
        profile.save()
        history = PointHistory()
        history.user_id = self.request.user.id
        title = Assignment.objects.get(id=self.kwargs['assignment_id']).title
        history.message = "繳交作業<"+title+">--2分"
        history.save()
        return valid
      
class AssignmentUpdate(UpdateView):
    model = Work
    fields = ['memo', "file"]
    success_url = "/student/classroom/"      
    template_name = "form.html"
    
class MemoList(generic.ListView):
    model = Work
    template_name = "student/memo_list.html"

    def get_context_data(self, **kwargs):
        context = super(MemoList, self).get_context_data(**kwargs)
        enrolls = Enroll.objects.filter(classroom_id=self.kwargs['classroom_id']).order_by("seat")
        student_ids = list(map(lambda a: a.student_id, enrolls))
        works = Work.objects.filter(assignment_id=self.kwargs['assignment_id'], student_id__in=student_ids)
        work_dict = dict((f.student_id, f) for f in works)
        memos = []
        for enroll in enrolls:
            if enroll.student_id in work_dict:
                memos.append([enroll, work_dict[enroll.student_id].memo, work_dict[enroll.student_id].publication_date])
            else :
                memos.append([enroll, "", None])
        context['memos'] = memos
        return context
      
class QuestionaryView(TemplateView):
    template_name = 'student/questionary_result.html'     

    # 限本班同學
    def render_to_response(self, context):
        if not is_classmate(self.request.user.id, self.kwargs['classroom_id']):
            return redirect('/')
        return super(QuestionaryView, self).render_to_response(context)         
      
    def get_context_data(self, **kwargs):
        context = super(QuestionaryView, self).get_context_data(**kwargs)
        classroom = Classroom.objects.get(id=self.kwargs['classroom_id'])
        enrolls = Enroll.objects.filter(classroom_id=classroom.id)
        student_ids = map(lambda a: a.student_id, enrolls)        
        q1 = ['q1',0,0,0,0]
        q2 = ['q2',0,0,0,0]
        q3 = ['q3',0,0,0,0]
        t1 = []
        t2 = []
        questionaries = Questionary.objects.filter(user_id__in=student_ids)
        for questionary in questionaries:
            q1[questionary.q1] += 1
            q2[questionary.q2] += 1            
            q3[questionary.q3] += 1            
            t1.append(questionary.t1)
            t2.append(questionary.t2)
        context['q1'] = q1
        context['q2'] = q2
        context['q3'] = q3
        context['t1'] = t1
        context['t2'] = t2
        context['questionaires']  = questionaries
        context['enrolls'] = enrolls
        context['classroom'] = classroom
        return context  
      
      