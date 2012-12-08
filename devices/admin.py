from django.contrib import admin
from models import Manufacture, Device, Configuration, Connection

admin.site.register(Manufacture)
admin.site.register(Device)
admin.site.register(Configuration)
admin.site.register(Connection)