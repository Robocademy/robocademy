from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Course, Video, QuestionAndAnswer
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    context = RequestContext(request, {'courses': Course.objects.all()}) 
    return render_to_response('interactive_courses/index.html', context)
    
def course(request, slug):
    context = RequestContext(request, {'course': Course.objects.get(slug=slug)})
    return render_to_response('interactive_courses/course_embed.html', context)
    
def course_embed(request, slug):
    context = RequestContext(request, {'course': Course.objects.get(slug=slug)})
    return render_to_response('interactive_courses/course_embed.html', context)    
    
def get_course_data(request, slug):
    course = Course.objects.get(slug=slug)
    response_data = {'lessons': [i.get_dict() for i in course.get_lessons()]}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
def course_admin(request, slug):
    context = RequestContext(request, {'course': Course.objects.get(slug=slug)})
    return render_to_response('interactive_courses/course_admin.html', context)
    
def admin_save(request, slug):
    course = Course.objects.get(slug=slug)
    course.title = request.POST['course_title']
    course.save()
    
    # get the lessons
    for lesson in course.get_lessons():
        lesson.title = request.POST['lesson_%s_title' % (lesson.order)]
        video = Video.objects.filter(lesson=lesson)[0]
        video.url = request.POST['lesson_%s_video_id' % (lesson.order)]
        video.save()
        question = QuestionAndAnswer.objects.filter(lesson=lesson)[0]
        question.statement = request.POST['lesson_%s_question' % (lesson.order)]
        question.save()
        
        # change answer choices
        for answer_choice in QuestionAndAnswer.objects.filter(lesson=lesson)[0].question_object.checkboxes.all().order_by('order'):
            answer_choice.value = request.POST['lesson_%s_answer_choice_%s' % (lesson.order, answer_choice.order)]
            answer_choice.save()
        
        lesson.save()
         
    
    return HttpResponse(str(request.POST))