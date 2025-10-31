from django.contrib import admin
from .models import Course, Enrollment, Lesson, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'difficulty', 'price', 'is_published', 'is_featured', 'enrollment_count', 'created_at']
    list_filter = ['category', 'difficulty', 'is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured']
    readonly_fields = ['created_at', 'updated_at', 'enrollment_count']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Course Details', {
            'fields': ('instructor', 'category', 'difficulty', 'thumbnail')
        }),
        ('Pricing', {
            'fields': ('is_free', 'price')
        }),
        ('Stats', {
            'fields': ('duration_hours', 'total_lessons')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'enrollment_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress', 'completed', 'enrolled_at', 'time_spent_minutes']
    list_filter = ['completed', 'enrolled_at', 'course__category']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at', 'last_accessed']
    
    fieldsets = (
        ('Enrollment Info', {
            'fields': ('user', 'course')
        }),
        ('Progress', {
            'fields': ('progress', 'completed', 'completed_at', 'time_spent_minutes')
        }),
        ('Timestamps', {
            'fields': ('enrolled_at', 'last_accessed')
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_published', 'is_preview']
    list_filter = ['is_published', 'is_preview', 'course']
    search_fields = ['title', 'course__title']
    list_editable = ['order', 'is_published', 'is_preview']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('course', 'title', 'description')
        }),
        ('Content', {
            'fields': ('video_url', 'content')
        }),
        ('Organization', {
            'fields': ('order', 'duration_minutes')
        }),
        ('Status', {
            'fields': ('is_published', 'is_preview')
        }),
    )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'lesson', 'completed', 'time_spent_minutes', 'completed_at']
    list_filter = ['completed', 'lesson__course']
    search_fields = ['enrollment__user__username', 'lesson__title']
    readonly_fields = ['completed_at']
