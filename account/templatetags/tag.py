from django import template
from django.contrib.auth.models import User, Group

register = template.Library()

@register.filter
def teacher_group(user):
    return user.groups.filter(name='teacher').exists()
  