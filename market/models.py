from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __unicode__(self):
        return self.name
    
class Idea(models.Model):
    summary = models.CharField(max_length=50)
    description = models.TextField()
    
    def __unicode__(self):
        return self.summary

class Entity(models.Model):
    name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name