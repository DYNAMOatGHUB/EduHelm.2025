from django.urls import path
from .views import TaskCreateView,TaskDetailView,TaskListView,TaskUpdateView,TaskDeleteView,task_toggle_complete

app_name = 'schedule'


urlpatterns=[
        path('task/new/',TaskCreateView.as_view(),name='task_create'),
        path('task/<int:pk>/',TaskDetailView.as_view(),name='task_detail'),
        path('',TaskListView.as_view(),name='task_list'),
        path('task/<int:pk>/edit',TaskUpdateView.as_view(),name='task_update'),
        path('task/<int:pk>/delete/',TaskDeleteView.as_view(),name='task_delete'),
        path('task/<int:pk>/toggle/', task_toggle_complete, name='task_toggle'),

]
