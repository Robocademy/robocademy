from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Device, Connection
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