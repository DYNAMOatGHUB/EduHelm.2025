from . import views
from .views import CourseListView,CourseDetailView,LessonDetailView
from django.urls import path



app_name = 'courses'

urlpatterns= [
    path('',CourseListView.as_view(),name='course_list'),
    path('<int:pk>/',CourseDetailView.as_view(),name='course_detail'),
    path('lesson/<int:pk>/',LessonDetailView.as_view(),name='lesson_detail'),
    path('lesson/<int:pk>/complete/',views.mark_lesson_complete,name='mark_lesson_complete'),
]
