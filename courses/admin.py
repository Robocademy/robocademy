from django.contrib import admin
from models import DeviceConfiguration, Lesson, ExecutedCode, CommandPattern

admin.site.register(DeviceConfiguration)
admin.site.register(Lesson)
admin.site.register(ExecutedCode)
admin.site.register(CommandPattern)