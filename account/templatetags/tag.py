from django import template
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from account.models import MessagePoll
from student.models import Work
from account.models import Profile
from account.models import Questionary

register = template.Library()

@register.filter
def teacher_group(user):
    return user.groups.filter(name='teacher').exists()
  
@register.filter
def teacher_classroom(user_id, classroom_id):
    classroom = Classroom.object.get(id=classroom_id)
    if classroom.teacher_id == user_id:
        return True
    else:
        return False

@register.filter(takes_context=True)
def realname(user_id):
    try: 
        user = User.objects.get(id=user_id)
        return user.first_name
    except :
        pass
    return ""
    
@register.filter(takes_context=True)
def read_already(message_id, user_id):
    try:
        messagepoll = MessagePoll.objects.get(message_id=message_id, reader_id=user_id)
    except ObjectDoesNotExist:
        messagepoll = MessagePoll()
    return messagepoll.read  
  
@register.filter(takes_context=True)
def work_exists(assignment_id, user_id):
    works = Work.objects.filter(assignment_id=assignment_id, student_id=user_id)
    if works.exists() :
        return True
    else:
        return False

@register.filter(takes_context=True)
def work_id(assignment_id, user_id):
    works = Work.objects.filter(assignment_id=assignment_id, student_id=user_id).order_by("-id")
    if works.exists() :
        return works[0].id
    else:
        return 0
      
@register.filter(takes_context=True)
def point(user):
    try:
        profile = Profile.objects.get(user=user)   
        return profile.point
    except ObjectDoesNotExist:
        return 0
      
@register.filter(takes_context=True)
def questionary_exists(user_id):
    try: 
        questionary = Questionary.objects.get(user_id=user_id)
        return True
    except ObjectDoesNotExist:
        return False      