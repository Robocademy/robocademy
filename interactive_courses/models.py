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
         
    def get_admin_url(self):
        return '/interactive_courses/%s/admin/' % (self.slug)       

    def delete_lessons(self):
        for i in Lesson.objects.filter(course=self):
            try:
                lesson_content = LessonContent.objects.get(lesson=self)
                lesson_content.delete()
            except:
                pass            
            try:
                display_after_video = DisplayAfterVideo.objects.get(lesson=self)
                display_after_video.delete()
            except:
                pass
            for j in Video.objects.filter(lesson=i):
                j.delete()
            for j in QuestionAndAnswer.objects.filter(lesson=i):
                for k in j.question_object.checkboxes.all():
                    k.delete()
                for k in j.answer_object.correct_checkboxes.all():
                    k.delete()    
                j.delete()
            i.delete()
        
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
        try:
            d.update({'video_id': Video.objects.filter(lesson=self)[0].url})
        except:
            pass
        try:
            lesson_content = LessonContent.objects.filter(lesson=self)[0]
            d.update({'content_type': lesson_content.type, 'content': lesson_content.content})
        except:
           pass
        d.update({'question': QuestionAndAnswer.objects.filter(lesson=self)[0].statement})
        try:
            d.update({'answer_choices': QuestionAndAnswer.objects.filter(lesson=self)[0].get_answer_choices()})
            d.update({'answer_ids': QuestionAndAnswer.objects.filter(lesson=self)[0].get_answer_ids()})
        except:
            pass
        try:
            d.update({'display_after_video': DisplayAfterVideo.objects.get(lesson=self).image})
        except:
            pass
        return d
        
    def display_after_video(self):
        return DisplayAfterVideo.objects.get(lesson=self)[0].image
        try:
            return DisplayAfterVideo.objects.get(lesson=self)[0].image
        except:
            return ''
        
    def get_video_id(self):
        try:
            return Video.objects.filter(lesson=self)[0].url
        except:
            return ''
            
    def get_content(self):
        return LessonContent.objects.filter(lesson=self)[0]    
        
    def content_type(self):
        return LessonContent.objects.filter(lesson=self)[0].type
        
    def content(self):
        return LessonContent.objects.filter(lesson=self)[0].content
        
    def get_question(self):
        return QuestionAndAnswer.objects.filter(lesson=self)[0].statement
        
    def get_questions(self):
        return [{'question': i.statement, 'answer_choices': i.get_answer_choices(), 'answer_ids': i.get_answer_ids(), 'order': int(i.order)} for i in QuestionAndAnswer.objects.filter(lesson=self)]
        
    def get_answer_choices(self):
        return QuestionAndAnswer.objects.filter(lesson=self)[0].get_answer_choices()

    def get_answer_ids(self):
        return QuestionAndAnswer.objects.filter(lesson=self)[0].get_answer_ids()      

            
        
class LessonContent(models.Model):
    lesson = models.ForeignKey(Lesson)
    type = models.CharField(max_length=50)
    content = models.TextField()    
        
    def __unicode__(self):
        return '%s: %s. %s %s' % (self.lesson.course.title, self.lesson.order, self.lesson.title, self.type)     
        
class Video(models.Model):
    lesson = models.ForeignKey(Lesson)
    url = models.CharField(max_length=200)
    provider = models.CharField(max_length=20)

    def __unicode__(self):
        return '%s: %s. %s' % (self.lesson.course.title, self.lesson.order, self.lesson.title)   
        
class DisplayAfterVideo(models.Model):
    lesson = models.ForeignKey(Lesson)
    image = models.CharField(max_length=200)
    
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
        return [{'id': int(i.id), 'value': i.value, 'order': int(i.order)} for i in self.question_object.checkboxes.all().order_by('order')]
        
    def get_answer_ids(self):
        return [int(i.id) for i in self.answer_object.correct_checkboxes.all().order_by('order')]
    
class CheckboxQuestion2(models.Model):
    checkboxes = models.ManyToManyField('Checkbox2')
    
class CheckboxAnswer2(models.Model):
    correct_checkboxes = models.ManyToManyField('Checkbox2')    
    
class Checkbox2(models.Model):
    
    order = models.PositiveIntegerField()
    value = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.value