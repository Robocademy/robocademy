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
        
    def get_url(self):
        return '/interactive_courses/%s/' % (self.slug)
        
    def get_lessons(self):
        return Lesson.objects.filter(course=self).order_by('order')
    
class CourseAuthorRelationship(models.Model):
    course = models.ForeignKey(Course)
    author = models.ForeignKey(User)
    order = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('course', 'order')
        
    def __unicode__(self):
        return '%s: %s. %s' % (self.course.title, self.order, self.author.get_full_name())  


class Lesson(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=50)
    slug = models.SlugField()
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ('course', 'order')
    
    def __unicode__(self):
        return '%s: %s. %s' % (self.course.title, self.order, self.title)  
    
    def get_dict(self, key_format=None):
        "Returns a dictionary containing field names and values for the given instance"
        instance = self
        from django.db.models.fields.related import ForeignKey
        from django.db.models import DateTimeField
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
                value = str(value)
            d[key(attr)] = value
        for field in instance._meta.many_to_many:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        d.update({'video_id': Video.objects.filter(lesson=self)[0].url})
        d.update({'question': QuestionAndAnswer.objects.filter(lesson=self)[0].statement})
        return d
    
        
class Video(models.Model):
    lesson = models.ForeignKey(Lesson)
    url = models.CharField(max_length=200)
    provider = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s: %s. %s' % (self.lesson.course.title, self.lesson.order, self.lesson.title)   
        
class QuestionAndAnswer(models.Model):
    lesson = models.ForeignKey(Lesson)
    order = models.PositiveIntegerField(default=1)
    statement = models.TextField()
    question_type = models.ForeignKey(ContentType, related_name="asQuestion")
    question_id = models.PositiveIntegerField()
    question_object = generic.GenericForeignKey('question_type', 'question_id')
    answer_type = models.ForeignKey(ContentType, related_name="asAnswer")
    answer_id = models.PositiveIntegerField()
    answer_object = generic.GenericForeignKey('answer_type', 'answer_id')    
    
    def __unicode__(self):
        return '%s: %s. %s %s' % (self.lesson.course.title, self.lesson.order, self.lesson.title, self.statement)  
        
    def get_answer_choices(self):
        return question_object.checkboxes.all().order_by('order').values_list('id', 'question')
        
    def get_answer_ids(self):
        return answer_object.checkboxes.all().values_list('id', flat=True)
    
class CheckboxQuestion2(models.Model):
    checkboxes = models.ManyToManyField('Checkbox2')
    
class CheckboxAnswer2(models.Model):
    correct_checkboxes = models.ManyToManyField('Checkbox2')    
    
class Checkbox2(models.Model):
    
    order = models.PositiveIntegerField()
    value = models.CharField(50)
    
    def __unicode__(self):
        return self.value