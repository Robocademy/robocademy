from django.db import models
from django.db.models import get_model
from django.contrib.auth.models import User

class Lesson(models.Model):
    device_configuration = models.ForeignKey('devices.Configuration')
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = (('device_configuration', 'name'),
                           ('device_configuration', 'order'))
                           
    def __unicode__(self):
        return '%s %s' % (self.device_configuration.device, self.device_configuration.name, self.order)