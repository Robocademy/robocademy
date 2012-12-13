from django.http import HttpResponse
from django.template import RequestContext
import json
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

def get_war_info(request):
    return render_to_response('', {})