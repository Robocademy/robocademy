from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User

class Manufacture(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.name    
    
class Device(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return self.name
        
        
    def get_configurations(self):
        Configuration = get_model('devices', 'configuration')
        return Configuration.objects.filter(device=self)
    
class Configuration(models.Model):
    device = models.ForeignKey(Device)
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return '%s %s' % (self.device, self.name)
    
    def get_dict(self, key_format=None):
        "Returns a dictionary containing field names and values for the given instance"
        instance = self
        from django.db.models.fields.related import ForeignKey
        if key_format:
            assert '%s' in key_format, 'key_format must contain a %s'
        key = lambda key: key_format and key_format % key or key

        d = {}
        for field in instance._meta.fields:
            attr = field.name
            value = getattr(instance, attr)
            if value is not None and isinstance(field, ForeignKey):
                value = value._get_pk_val()
            d[key(attr)] = value
        for field in instance._meta.many_to_many:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        d.update({'stream': self.get_connection()})
        return d
    
    def get_lessons(self):
        Lesson = get_model('lessons', 'lesson')
        return Lesson.objects.filter(device_configuration=self)
        
    def get_connection(self):    
        Connection = get_model('devices', 'Connection')
        return Connection.objects.filter(configuration=self)[0].stream
    
class Connection(models.Model):
    configuration = models.ForeignKey(Configuration)
    stream = models.CharField(max_length=200)
    streaming_provider = models.CharField(max_length=50)
    
    
    def __unicode__(self):
        return '%s %s' % (self.configuration.device, self.configuration.name)
        
    def get_dict(self, key_format=None):
        "Returns a dictionary containing field names and values for the given instance"
        instance = self
        from django.db.models.fields.related import ForeignKey
        if key_format:
            assert '%s' in key_format, 'key_format must contain a %s'
        key = lambda key: key_format and key_format % key or key

        d = {}
        for field in instance._meta.fields:
            attr = field.name
            value = getattr(instance, attr)
            if value is not None and isinstance(field, ForeignKey):
                value = value._get_pk_val()
            d[key(attr)] = value
        for field in instance._meta.many_to_many:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        d.update({'stream': self.get_connection()})
        return d
        
class UsersCode(models.Model):
    connection = models.ForeignKey(Connection)   
    code = models.TextField()
    
class CodeStatus(models.Model):
    connection = models.ForeignKey(Connection)   
    status = models.BooleanField()
    
class CodeExample(models.Model):
    connection = models.ForeignKey(Connection)   
    added_by = models.ForeignKey(User, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, unique=True)
    code = models.TextField()
    
    def get_dict(self, key_format=None):
        "Returns a dictionary containing field names and values for the given instance"
        instance = self
        from django.db.models.fields.related import ForeignKey, DateTimeField
        if key_format:
            assert '%s' in key_format, 'key_format must contain a %s'
        key = lambda key: key_format and key_format % key or key

        d = {}
        for field in instance._meta.fields:
            attr = field.name
            value = getattr(instance, attr)
            if value is not None and isinstance(field, ForeignKey):
                value = value._get_pk_val()
            elif isinstance(field, DateTimeField): 
                value = str(value._get_pk_val())
            d[key(attr)] = value
        for field in instance._meta.many_to_many:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        return d

class CmdStatus(models.Model):
    connection = models.ForeignKey(Connection)   
    status = models.TextField()
    
class SerialMonitor(models.Model):
    connection = models.ForeignKey(Connection)   
    content = models.TextField()
    
    
class ExecutedCode(models.Model):
    
    connection = models.ForeignKey(Connection)   
    user = models.ForeignKey(User, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    
    