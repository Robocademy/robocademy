from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Course, Lesson, Video, QuestionAndAnswer, CheckboxQuestion2, CheckboxAnswer2, Checkbox2
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

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
    
@staff_member_required    
def course_admin(request, slug):
    context = RequestContext(request, {'course': Course.objects.get(slug=slug)})
    return render_to_response('interactive_courses/course_admin.html', context)
import re
    
@staff_member_required
def admin_save(request, slug):
    #request.POST = dict([(x, y[0]) for x, y in request.POST.items()])
    #return HttpResponse(str(request.POST))
    course = Course.objects.get(slug=slug)
    #course.title = request.POST['course_title']
    course.save()
    course.delete_lessons()
    last_lesson = max([int(re.search('\w+_(?P<n>\d+)_\w+', i).group('n')) for i in request.POST.keys() if re.match('\w+_(?P<n>\d+)_\w+', i)])
    for lesson_order in range(1, last_lesson + 1):
        lesson = Lesson(course=course, order=lesson_order, title=request.POST['lesson_%s_title' % (lesson_order)])
        lesson.save()
        video = Video(lesson=lesson, url=request.POST['lesson_%s_video_id' % (lesson_order)], provider='youtube')
        video.save()
        last_question = max([int(re.search('\w+_%s_\w+_(?P<n>\d+)' % (lesson_order), i).group('n')) for i in request.POST.keys() if re.match('\w+_%s_\w+_(?P<n>\d+)' % (lesson_order), i)])
        for question_order in range(1, last_question + 1):
            #checkboxes
            checkbox_question = CheckboxQuestion2()
            checkbox_answer = CheckboxAnswer()
            for h, cq in enumerate(sorted([i for i in request.POST.keys() if re.match('\w+_%s_question_%s_answer_choice_\d+' % (lesson_order, answer_choice)), i)])):
                checkbox = Checkbox2(order=h, value=request.POST['cq'])
                checkbox.save()
                checkbox_question.checkboxes.add(checkbox)
                if request.POST[cq.replace('answer_choice', 'answer')] == 'true':
                    checkbox_answer.checkboxes.add(checkbox)
            checkbox_question.save()
            question = QuestionAndAnswer(lesson=lesson, order=question_order, 
                statement=request.POST['lesson_%s_question_%s' % (lesson_order, question_order)],
                question_type=ContentType.objects.get(app_label="interactive_courses", model="CheckboxQuestion2"),
                question_id=checkbox_question.id,
                answer_type=ContentType.objects.get(app_label="interactive_courses", model="CheckboxAnswer2"),
                answer_id=checkbox_answer.id)
            question.statement = request.POST['lesson_%s_question' % (lesson_order)]
            question.save()
        
    #return HttpResponse(str(request.POST))
    # get the lessons
    #for lesson in course.get_lessons():
    #    lesson.title = request.POST['lesson_%s_title' % (lesson.order)]
    #    video = Video.objects.filter(lesson=lesson)[0]
    #    video.url = request.POST['lesson_%s_video_id' % (lesson.order)]
    #    video.save()
    #    question = QuestionAndAnswer.objects.filter(lesson=lesson)[0]
    #    question.statement = request.POST['lesson_%s_question' % (lesson.order)]
    #    question.save()
        
        # change answer choices
    #    for answer_choice in QuestionAndAnswer.objects.filter(lesson=lesson)[0].question_object.checkboxes.all().order_by('order'):
    #        answer_choice.value = request.POST['lesson_%s_answer_choice_%s' % (lesson.order, answer_choice.order)]
    #        answer_choice.save()
        
    #    lesson.save()
         
    
    return HttpResponse(str(request.POST))