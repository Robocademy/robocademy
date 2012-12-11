from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Course(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    price = models.FloatField(default=0)
    authors = models.ManyToManyField(User, through='CourseAuthorRelationship')
    
    def __unicode__(self):
        return self.title
    
class CourseAuthorRelationship(models.Model):
    course = models.ForeignKey(Course)
    author = models.ForeignKey(User)
    order = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%s: %s. %s' % (self.course.title, self.order, self.author.get_full_name())  
    
    class Meta:
        unique_together = ('course', 'order')

class Lesson(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    order = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%s: %s. %s' % (self.course.title, self.order, self.title)  
    
    class Meta:
        unique_together = ('course', 'order')
        
class QuestionAndAnswer(models.Model):
    lesson = models.ForeignKey(Lesson)
    order = models.PositiveIntegerField(default=0)
    statement = models.TextField()
    question_type = models.ForeignKey(ContentType)
    question_id = models.PositiveIntegerField()
    question_object = generic.GenericForeignKey('question_type', 'question_id')
    answer_type = models.ForeignKey(ContentType)
    answer_id = models.PositiveIntegerField()
    answer_object = generic.GenericForeignKey('answer_type', 'answer_id')    
    
    def __unicode__(self):
        return '%s: %s. %s' % (self.lesson.course.title, self.lesson.order, self.lesson.title, self.statement)  
    
class CheckboxQuestion(models.Model):
    checkboxes = models.ManyToManyField('Checkbox')
    
class CheckboxAnswer(models.Model):
    correct_checkboxes = models.ManyToManyField('Checkbox')    
    
class Checkbox(models.Model):
    question = models.ForeignKey(CheckboxQuestion)
    order = models.PositiveIntegerField()
    