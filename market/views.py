from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Category, Entity, Idea
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

def index(request):
    context = RequestContext(request, {'categories': [i.category for i in CategoryOrder.objects.all().order_by('order')]}) 
    return render_to_response('market/index.html', context)