from .models import StudyTask
from django import forms


class StudyTaskForm(forms.ModelForm):
    class Meta:
         model=StudyTask
         fields=['title','content','due_date']

         widgets = {
                    'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
         }


