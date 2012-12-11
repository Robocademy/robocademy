from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Course
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required