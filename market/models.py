from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
class Idea(models.Model):
    summary = models.CharField(max_length=50)
    description = models.TextField()

class Enity(models.Model):
    name = models.CharField(max_length=50)