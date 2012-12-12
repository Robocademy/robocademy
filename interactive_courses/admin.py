from django.contrib import admin
from models import Course, CourseAuthorRelationship, Lesson, QuestionAndAnswer, CheckboxQuestion2, CheckboxAnswer2, Checkbox2, Video

admin.site.register(Course)
admin.site.register(CourseAuthorRelationship)
admin.site.register(Lesson)
admin.site.register(QuestionAndAnswer)
admin.site.register(CheckboxQuestion2)
admin.site.register(CheckboxAnswer2)
admin.site.register(Checkbox2)
admin.site.register(Video)