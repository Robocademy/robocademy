from django.http import HttpResponse
from django.template import RequestContext
import json

from django.shortcuts import render_to_response


def arduino_expert(request):
    #context = RequestContext(request, {'lessons': Lesson.objects.filter(device_configuration__id=1).order_by('order')})
    #context.update({'examples': Code.objects.all(), 'default_example': Lesson.objects.get(device_configuration__id=1, order=1).start_code})
    #context.update({'examples': Code.objects.all(), 'default_example': Code.objects.get(title='Hello World').code})
    return render_to_response('courses/arduino_expert.html', {})    
    
