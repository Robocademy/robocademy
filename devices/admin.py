from django.contrib import admin
from models import Manufacture, Device, Configuration, Connection, UsersCode, CodeStatus, CodeExample, CmdStatus, SerialMonitor, ExecutedCode

admin.site.register(Manufacture)
admin.site.register(Device)
admin.site.register(Configuration)
admin.site.register(Connection)
admin.site.register(UsersCode)
admin.site.register(CodeStatus)
admin.site.register(CodeExample)
admin.site.register(CmdStatus)
admin.site.register(SerialMonitor)
admin.site.register(ExecutedCode)