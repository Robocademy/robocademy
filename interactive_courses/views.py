from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Course
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    context = RequestContext(request, {'courses': Course.objects.all()}) 
    return render_to_response('interactive_courses/index.html', context)
    
def course(request, slug):
    context = RequestContext(request, {'course': Course.objects.get(slug=slug)})
    return render_to_response('interactive_courses/course_embed.html', context)
    
def get_course_data(request, slug):
    course = Course.objects.get(slug=slug)
    response_data = {'lessons': [i.get_dict() for i in course.get_lessons()]}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")