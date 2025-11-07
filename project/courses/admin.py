from django.contrib import admin
from .models import Course, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson_course', 'lesson_order', 'youtube_id']
    list_filter = ['lesson_course']
    search_fields = ['title', 'lesson_course__title']
    list_editable = ['lesson_order']


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'lesson_link', 'is_completed']
    list_filter = ['is_completed', 'lesson_link__lesson_course']
    search_fields = ['user_link__username', 'lesson_link__title']
