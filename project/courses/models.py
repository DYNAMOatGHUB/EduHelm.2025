from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Course(models.Model):
    """Model representing a course in the learning platform"""
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('data_science', 'Data Science'),
        ('web_dev', 'Web Development'),
        ('mobile_dev', 'Mobile Development'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Course Details
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    
    # Media
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    
    # Pricing
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, help_text="Price in USD")
    is_free = models.BooleanField(default=True)
    
    # Course Stats
    duration_hours = models.PositiveIntegerField(default=0, help_text="Estimated course duration in hours")
    total_lessons = models.PositiveIntegerField(default=0)
    
    # Status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    @property
    def enrollment_count(self):
        return self.enrollment_set.count()


class Enrollment(models.Model):
    """Model representing a user's enrollment in a course"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_set')
    
    # Progress Tracking
    progress = models.FloatField(default=0.0, help_text="Progress percentage (0-100)")
    completed = models.BooleanField(default=False)
    
    # Timestamps
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    
    # Study Time
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
    
    def mark_complete(self):
        """Mark the enrollment as completed"""
        from django.utils import timezone
        self.completed = True
        self.progress = 100.0
        self.completed_at = timezone.now()
        self.save()


class Lesson(models.Model):
    """Model representing a lesson within a course"""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Content
    video_url = models.URLField(blank=True, null=True, help_text="YouTube or Vimeo URL")
    content = models.TextField(blank=True, help_text="Lesson content/notes")
    
    # Organization
    order = models.PositiveIntegerField(default=0, help_text="Order within the course")
    duration_minutes = models.PositiveIntegerField(default=0)
    
    # Status
    is_published = models.BooleanField(default=True)
    is_preview = models.BooleanField(default=False, help_text="Can be viewed without enrollment")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['course', 'order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LessonProgress(models.Model):
    """Track user progress on individual lessons"""
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['enrollment', 'lesson']
        verbose_name = 'Lesson Progress'
        verbose_name_plural = 'Lesson Progress'
    
    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.enrollment.user.username} - {self.lesson.title} ({status})"
