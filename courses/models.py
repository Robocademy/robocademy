from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User

class UsersCode(models.Model):
    code = models.TextField()
    
class CodeStatus(models.Model):
    stauts = models.BooleanField()
    
class Code(models.Model):
    added_by = models.ForeignKey(User)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, unique=True)
    code = models.TextField()

class CmdStatus(models.Model):
    status = models.TextField()
    
class SerialMonitor(models.Model):
    content = models.TextField()
    
class DeviceConfiguration(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
class Lesson(models.Model):
    device_configuration = models.ForeignKey(DeviceConfiguration)
    order = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    summary = models.TextField(blank=True)
    start_code = models.TextField()
    stop_code = models.TextField()
    video = models.CharField(max_length=500, blank=True)
    
    def __unicode__(self):
        return '%s. %s' % (self.order, self.name)
    
    def get_command_pattern(self):
        try:
            CommandPattern = get_model('courses', 'CommandPattern')
            return CommandPattern.objects.get(lesson=self).pattern
        except:
            return None
    
class ExecutedCode(models.Model):
    #device_configuration = models.ForeignKey(DeviceConfiguration, null=True, blank=True)
    lesson = models.ForeignKey(DeviceConfiguration, null=True, blank=True)    
    user = models.ForeignKey(User, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    code = models.TextField()

class CommandPattern(models.Model):
    lesson = models.OneToOneField(Lesson)
    pattern = models.CharField(max_length=1000)
    
    