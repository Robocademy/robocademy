from django.http import HttpResponse
from django.template import RequestContext
import json
from models import Category, Entity, Idea, CategoryOrder
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType

def index(request):
    try:
        companies = ['Abar Automation', 'ABB', 'Accuworx', 'Adept Technology', 'Advanced Coating Robotics', 'Advanced Robotic Technology', 'Aerotech', 'Aetnagroup SpA', 'AIDA Engineering (JP)', 'Alaark Robotics, Inc.', 'Alfa Automation Technology Ltd', 'Alpha Robotics', 'American Robot', 'American Robot Sales', 'Antenen Research', 'Apex Automation & Robotics', 'Applied Controls Technology', 'ARC Specialities, Inc.', 'Asic Robotics AG', 'Aspect Automation', 'ASS End of Arm Tooling', 'Atlas Copco AB', 'ATM Automation Ltd.', 'ATS Automation Tooling Systems', 'Aurotek Corp', 'Austong Intelligent Robot Technology (CN)', 'Automatted Motion', 'AVN Gruppen', 'AWL Techniek (NV)', 'Axium, Inc.', 'Baumann Automation', 'Bila A/S', 'BL Autotec, Ltd.', 'Bleichert, Inc.', 'Bosch', 'Braas Co', 'Brokk AB', 'Chad Industries', 'Chariot Robotics', 'CIM Systems, Inc.', 'Cimcorp Oy', 'Cloos Schweisstechnik Robotic', 'CMA Robotics', 'Columbia/Okura, LLC', 'Comau', 'Conair Group', 'Creative Automation', 'CT Pack Srl (IT)', 'Daewoo Shipbuilding & Marine Engr', 'Daihen Corp.', 'DanRob', 'Daum + Partner GmbH', 'Dematic GmbH', 'Denso-Wave Robotics', 'DiFacto Robotics & Automation', 'Dong-Hyun Systems (DHS)', 'Dongbu Robot (prev DasaRobot) (KR)', 'Dover Corp (DE-STA-CO)', 'Duepi Automazioni Industriali', 'Durr Systems', 'Dynamic Motion Technology', 'Dynax (JP)', 'Egemin Automation', 'Electroimpact Inc.', 'Electtric80 (IT)', 'Ellison Technologies Automation', 'ENGEL Austria GmbH', 'Erowa Technology', 'EWAB Engineering', 'Fanuc', 'Farr Automation, Inc.', 'Fatronik Technalia', 'FerRobotics GmbH', 'FIPA GmbH', 'FleetwoodGoldcoWyard', 'Flexilane (WIKA Systems) (Denmark)', 'FlexLink', 'Fronius IG', 'Fuji Yusoki Kogyou', 'Gema Switzerland GmbH', 'Gerhard Schubert GmbH', 'GHS Automation', 'Gibotech A/S', 'Glama Engineering', 'GM Global Tech Ops', 'Gotting KG', 'Gudel Robotics', 'H.A.P. GmbH', 'Harly Robotic-Arm Co., Ltd.', 'Harmo (JP)', 'Hitachi Kokusai Electric Inc.', 'Hon Hai Precision (Foxconn)', 'Honeywell', 'Huaxing Machinery Corp', 'Hyundai Heavy Industries (KR)', 'I&J Fisnar', 'IAI America', 'IGM Robotic Systems AG', 'IHI Group', 'Industrial Control Repair']
        for comapny in companies:
            entity = Entity(name=company)
            entity.save()

    except:
        pass
    context = RequestContext(request, {'categories': [i.category for i in CategoryOrder.objects.all().order_by('order')], 'companies': Entity.objects.all()}) 
    return render_to_response('market/index.html', context)