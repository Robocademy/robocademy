from django.contrib import admin
from models import Course, CourseAuthorRelationship, Lesson, QuestionAndAnswer, CheckboxQuestion, CheckboxAnswer, Checkbox, Video

admin.site.register(Course)
admin.site.register(CourseAuthorRelationship)
admin.site.register(Lesson)
admin.site.register(QuestionAndAnswer)
admin.site.register(CheckboxQuestion)
admin.site.register(CheckboxAnswer)
admin.site.register(Checkbox)
admin.site.register(Video)