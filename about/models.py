from django.db.models import get_model
from django.db import models
from django.contrib.auth.models import User

class Contributor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    summary = models.CharField(max_length=500, blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.name, self.summary)   