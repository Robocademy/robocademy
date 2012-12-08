from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Device, Connection, UsersCode, CodeStatus, Example, CmdStatus, SerialMonitor, ExecutedCode
from django.shortcuts import render_to_response

def get_dropdown_tree(request):
    tree =[[device.name, [configuration.get_dict() for configuration in device.get_configurations()]] for device in Device.objects.all()]
    response_data = tree
    return HttpResponse(json.dumps(response_data), mimetype="application/json")

def get_connections():
    return Connection.objects.all()
    
def device_connections(request):
    
    return render_to_response('devices/connections.html', {'connections': get_connections()})

    
    
def device_connections_json(request):
    response_data = get_connections()
    return HttpResponse(json.dumps(response_data), mimetype="application/json")   
    
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
    if CmdStatus.objects.filter(connection__id=connection_id):
        return HttpResponse(str(CmdStatus.objects.filter(connection__id=connection_id)[0].status), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_cmd_status(request, connection_id):
    for i in CmdStatus.objects.all():
        i.delete()
    status = CmdStatus(status=request.POST['status'])
    status.save()
    return HttpResponse(status.status)
    
def get_serial_monitor(request, connection_id):
    if SerialMonitor.objects.filter(connection__id=connection_id):
        return HttpResponse(str(SerialMonitor.objects.all()[0].content), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_serial_monitor(request):
    for i in SerialMonitor.objects.all():
        i.delete()
    content = request.POST['content']
    connection_id = request.POST['connection_id']
    content = "".join([x if ord(x) < 128 else '' for x in content])
    sm = SerialMonitor(content=content, connection__id=connection_id)
    sm.save()
    return HttpResponse(sm.content, content_type="text/plain")
        
def set_status(request, connection_id):

    for i in CodeStatus.objects.filter(connection__id=connection_id):
        i.delete()
    status = CodeStatus(connection__id=connection_id, status=True)
    status.save()
    return HttpResponse('')

def get_example_code(request):
    example_id = request.GET['id']
    response_data = {'code': Code.objects.get(id=example_id).code}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")