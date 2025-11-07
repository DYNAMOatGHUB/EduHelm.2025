from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(default='course_default.jpg',upload_to='course_pics')

    def __str__(self):
        return self.title           #when other DB link to this DB .they use the title as a primary key to link here

class Lesson(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    youtube_id=models.CharField(max_length=20)   # cause the standard YouTube ID is only 11 characters
    lesson_order=models.IntegerField(default=0)
    lesson_course=models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class LessonProgress(models.Model):
    user_link=models.ForeignKey(User,on_delete=models.CASCADE)
    lesson_link=models.ForeignKey(Lesson,on_delete=models.CASCADE)
    is_completed=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_link.username}-{self.lesson_link.title}'
