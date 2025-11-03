from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView,DetailView,ListView,UpdateView,DeleteView
from .models import StudyTask
from .forms import StudyTaskForm # Corrected import line

class TaskListView(ListView):
    model=StudyTask
    template_name='schedule/task_list.html'

    def get_queryset(self):
        return StudyTask.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # This adds the current time to the template as a variable
        context['current_time'] = timezone.now()
        return context



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = StudyTask
    form_class = StudyTaskForm
    template_name = 'schedule/task_form.html'
    success_url = reverse_lazy('schedule:task_list')
    # NOTE: Add a success_url attribute here if you rely on static redirect  "static redirect " means just redirect to the exact location mentioned .unlike get_absolute_url which changes the location based on the pk
    # success_url = reverse_lazy('sample_home')

    def form_valid(self, form):
        # Attaches the current logged-in user as the author before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = StudyTask
    template_name = 'schedule/task_detail.html'

    # CORRECTED METHOD NAME: get_queryset
    def get_queryset(self):
        # This crucial line ensures the user can only retrieve tasks they own.
        return StudyTask.objects.filter(author=self.request.user)


class TaskUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = StudyTask
    form_class= StudyTaskForm
    template_name = 'schedule/task_form.html'

    def test_func(self):
        task=self.get_object()      # Get the specific task object the user is trying to edit
        if self.request.user== task.author:
            return True
        return False

class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=StudyTask
    template_name='schedule/task_confirm_delete.html'
    success_url=reverse_lazy('schedule:task_list')

    def test_func(self):
        task=self.get_object()
        if task.author == self.request.user:
            return True
        return False


def task_toggle_complete(request, pk):
    # Get the specific task, ensuring it belongs to the logged-in user
    task = get_object_or_404(StudyTask, pk=pk, author=request.user)

    # We only process POST requests
    if request.method == 'POST':
        # Toggle the boolean field
        task.is_completed = not task.is_completed
        task.save()

    # Redirect back to the task list
    return redirect('schedule:task_list')



