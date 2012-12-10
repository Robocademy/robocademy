from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Device, Connection, UsersCode, CodeStatus, CodeExample, CmdStatus, SerialMonitor, ExecutedCode
from django.shortcuts import render_to_response

def get_dropdown_tree(request):
    tree = [[device.name, [configuration.get_dict() for configuration in device.get_configurations()]] for device in Device.objects.all()]
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
    connection = Connection.objects.get(id=request.POST['connection_id'])
    example = Example(added_by=request.user, title=request.POST['title'], code=request.POST['code'], connection=connection)
    example.save()
    return HttpResponse('')
    
def send_code(request):
    connection = Connection.objects.get(id=request.POST['connection_id'])
    for i in UsersCode.objects.filter(connection=connection):
        i.delete()
    code = request.POST['code']
    users_code = UsersCode(connection=connection, code=code)
    users_code.save()
    for i in CodeStatus.objects.filter(connection=connection):
        i.delete()
    status = CodeStatus(connection=connection, status=False)
    status.save()
    if request.user.is_authenticated():
        executed_code = ExecutedCode(connection=connection, code=code, user=request.user)
    else:
        executed_code = ExecutedCode(connection=connection, code=code)
    executed_code.save()
    return HttpResponse(str(users_code.id) + '\n' + users_code.code)

def get_code(request, connection_id):
    try:
        connection = Connection.objects.get(id=connection_id)
        users_code = UsersCode.objects.filter(connection=connection)[0]
        code = str(users_code.id) + '\n' + users_code.code
        return HttpResponse(code, content_type="text/plain")
    except:
        return HttpResponse('None', content_type="text/plain")
        
def get_status(request, connection_id):
    try:
        connection = Connection.objects.get(id=connection_id)
        return HttpResponse(str(CodeStatus.objects.filter(connection=connection)[0].status), content_type="text/plain")
    except:
        return HttpResponse('False', content_type="text/plain")
 
def get_cmd_status(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    if CmdStatus.objects.filter(connection=connection):
        return HttpResponse(str(CmdStatus.objects.filter(connection=connection)[0].status), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_cmd_status(request):
    connection = Connection.objects.get(id=request.POST['connection_id'])
    for i in CmdStatus.objects.filter(connection=connection):
        i.delete()
    status = CmdStatus(connection=connection, status=request.POST['status'])
    status.save()
    return HttpResponse(status.status)
    
def get_serial_monitor(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    if SerialMonitor.objects.filter(connection=connection):
        return HttpResponse(str(SerialMonitor.objects.all()[0].content), content_type="text/plain")
    return HttpResponse('', content_type="text/plain")
 
def set_serial_monitor(request):
    connection = Connection.objects.get(id=request.POST['connection_id'])
    for i in SerialMonitor.objects.filter(connection=connection):
        i.delete()
    content = request.POST['content']
    content = "".join([x if ord(x) < 128 else '' for x in content])
    sm = SerialMonitor(content=content, connection=connection)
    sm.save()
    return HttpResponse(sm.content, content_type="text/plain")
        
def get_start_code(request, connection_id):
    connection = Connection.objects.(id=connection_id)
    start_code = StartCode.objects.filter(connection=connection)
    if start_code:
        start_code = start_code[0].code
    else:
        start_code = ''
    return HttpResponse(start_code, content_type="text/plain")
        
def get_examples(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    response_data = [i.get_dict() for i in CodeExample.objects.filter(connection=connection)]
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
def set_status(request, connection_id):
    connection = Connection.objects.get(id=connection_id)
    for i in CodeStatus.objects.filter(connection=connection):
        i.delete()
    status = CodeStatus(connection=connection, status=True)
    status.save()
    return HttpResponse('')

def get_example_code(request, connection_id):
    example_id = request.GET['id']
    response_data = {'code': Code.objects.get(id=example_id).code}
    return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
def get_connection_id(request, stream_id):
    return HttpResponse(Connection.objects.get(stream=stream_id).id)