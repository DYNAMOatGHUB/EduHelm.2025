from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class StudyTask(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField(blank=True,null=True)
    due_date=models.DateTimeField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    is_completed=models.BooleanField(default=False)
    author=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('schedule:task_detail',kwargs={'pk':self.pk})