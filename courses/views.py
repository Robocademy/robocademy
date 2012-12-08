from django.http import HttpResponse
from models import UsersCode
from models import CodeStatus
from models import CmdStatus
from models import Code
from models import SerialMonitor
from models import DeviceConfiguration, Lesson, ExecutedCode
from django.template import RequestContext
import json

from django.shortcuts import render_to_response

def arduino(request):
    context = RequestContext(request, {'lessons': Lesson.objects.filter(device_configuration__id=1).order_by('order')})
    context.update({'examples': Code.objects.all(), 'default_example': Lesson.objects.get(device_configuration__id=1, order=1).start_code})
    #context.update({'examples': Code.objects.all(), 'default_example': Code.objects.get(title='Hello World').code})
    return render_to_response('courses/arduino.html', context)

def arduino_expert(request):
    #context = RequestContext(request, {'lessons': Lesson.objects.filter(device_configuration__id=1).order_by('order')})
    #context.update({'examples': Code.objects.all(), 'default_example': Lesson.objects.get(device_configuration__id=1, order=1).start_code})
    #context.update({'examples': Code.objects.all(), 'default_example': Code.objects.get(title='Hello World').code})
    return render_to_response('courses/arduino_expert.html', {})    
    
def save_example(request):
    example = Code(added_by=request.user, title=request.POST['title'], code=request.POST['code'])
    example.save()
    return HttpResponse('')
    
def send_code(request):
    for i in UsersCode.objects.all():
        i.delete()
    code = request.POST['code']
    users_code = UsersCode(code=code)
    users_code.save()
    for i in CodeStatus.objects.all():
        i.delete()
    status = CodeStatus(stauts=False)
    status.save()
    if request.user.is_authenticated():
        executed_code = ExecutedCode(code=code, user=request.user)
    else:
        executed_code = ExecutedCode(code=code)
    executed_code.save()
    return HttpResponse(str(users_code.id) + '\n' + users_code.code)

def get_code(request):
    try:
        users_code = UsersCode.objects.all()[0]
        code = str(users_code.id) + '\n' + users_code.code
        return HttpResponse(code, content_type="text/plain")
    except:
        return HttpResponse('None', content_type="text/plain")
        
def get_status(request):
    try:
        return HttpResponse(str(CodeStatus.objects.all()[0].stauts), content_type="text/plain")
    except:
        return HttpResponse('False', content_type="text/plain")
 
def get_cmd_status(request):
    if CmdStatus.objects.all():
        return HttpResponse(str(CmdStatus.objects.all()[0].status), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_cmd_status(request):
    for i in CmdStatus.objects.all():
        i.delete()
    status = CmdStatus(status=request.POST['status'])
    status.save()
    return HttpResponse(status.status)
    
def get_serial_monitor(request):
    if SerialMonitor.objects.all():
        return HttpResponse(str(SerialMonitor.objects.all()[0].content), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_serial_monitor(request):
    for i in SerialMonitor.objects.all():
        i.delete()
    content = request.POST['content']
    content = "".join([x if ord(x) < 128 else '' for x in content])
    sm = SerialMonitor(content=content)
    sm.save()
    return HttpResponse(sm.content, content_type="text/plain")
        
def set_status(request):
    for i in CodeStatus.objects.all():
        i.delete()
    status = CodeStatus(stauts=True)
    status.save()
    return HttpResponse('')

def get_example_code(request):
    example_id = request.GET['id']
    response_data = {'code': Code.objects.get(id=example_id).code}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
def test_command(request):
    lesson = Lesson.objects.get(id=request.POST['lesson_id'])
    command = request.POST['command']
        
    
def test_code(request):
    import re
    code = request.POST['code']
    led_sign_set_pattern = 'LedSign::Set\((?P<col>\d+)\s*?,\s*?(?P<row>\d)+\s*?,\s*?1\);'
    m = re.search(led_sign_set_pattern, code)
    if m:
        response_data = {'ready': True}
    else:
        response_data = {'ready': False}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")    
    
def get_lessons(request, device_configuration_id):
    lessons = Lesson.objects.filter(device_configuration__id=device_configuration_id).order_by('order')
    lessons = [{'id': i.id, 'name': i.name, 'command_pattern': i.get_command_pattern(), 'summary': i.summary, 'stop_code': i.stop_code} for i in lessons]
    response_data = {'lessons': lessons}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")    