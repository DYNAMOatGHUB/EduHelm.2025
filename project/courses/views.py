from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Course, Enrollment, Lesson, LessonProgress
import logging

logger = logging.getLogger(__name__)


def course_list(request):
    """Display all published courses"""
    # Djongo struggles with is_published=True + JOIN, so fetch all and filter in Python
    try:
        all_courses = list(Course.objects.select_related('instructor'))
        courses = [c for c in all_courses if c.is_published]
    except Exception as exc:
        logger.error("Failed to load courses: %s", exc)
        courses = []
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        courses = [c for c in courses if c.category == category]
    
    # Filter by difficulty
    difficulty = request.GET.get('difficulty')
    if difficulty:
        courses = [c for c in courses if c.difficulty == difficulty]
    
    # Search
    search = request.GET.get('search')
    if search:
        courses = [c for c in courses if search.lower() in c.title.lower()]
    
    # Sort by created_at descending (newest first)
    courses.sort(key=lambda c: c.created_at, reverse=True)
    
    context = {
        'courses': courses,
        'categories': Course.CATEGORY_CHOICES,
        'difficulties': Course.DIFFICULTY_LEVELS,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    """Display course details"""
    # Fetch course - Djongo may struggle with is_published filter
    try:
        course = Course.objects.select_related('instructor').get(slug=slug)
        if not course.is_published:
            from django.http import Http404
            raise Http404("Course not found")
    except Course.DoesNotExist:
        from django.http import Http404
        raise Http404("Course not found")
    
    # Get published lessons
    all_lessons = list(course.lessons.all())
    lessons = [l for l in all_lessons if l.is_published]
    lessons.sort(key=lambda l: l.order)
    
    # Check if user is enrolled
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    """Enroll user in a course"""
    try:
        course = Course.objects.get(slug=slug)
        if not course.is_published:
            messages.error(request, 'This course is not available.')
            return redirect('course_list')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('course_list')
    
    # Check if already enrolled
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}')
    
    return redirect('course_detail', slug=course.slug)


@login_required
def my_courses(request):
    """Display user's enrolled courses"""
    # Fetch enrollments without select_related to avoid Djongo issues
    enrollments = list(Enrollment.objects.filter(user=request.user))
    
    # Calculate statistics
    total_enrollments = len(enrollments)
    completed_count = len([e for e in enrollments if e.completed])
    
    # Calculate average progress
    if total_enrollments > 0:
        total_progress = sum(e.progress for e in enrollments)
        average_progress = total_progress / total_enrollments
    else:
        average_progress = 0
    
    context = {
        'enrollments': enrollments,
        'total_enrollments': total_enrollments,
        'completed_count': completed_count,
        'average_progress': average_progress,
    }
    return render(request, 'courses/my_courses.html', context)


@login_required
def lesson_view(request, course_slug, lesson_id):
    """View a specific lesson"""
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Check enrollment
    try:
        enrollment = Enrollment.objects.get(user=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'You must enroll in this course first.')
        return redirect('course_detail', slug=course_slug)
    
    # Get or create lesson progress
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    # Get all published lessons for navigation
    all_lessons_raw = list(course.lessons.all())
    all_lessons = [l for l in all_lessons_raw if l.is_published]
    all_lessons.sort(key=lambda l: l.order)
    
    context = {
        'course': course,
        'lesson': lesson,
        'progress': progress,
        'all_lessons': all_lessons,
        'enrollment': enrollment,
    }
    return render(request, 'courses/lesson_view.html', context)


@login_required
def mark_lesson_complete(request, course_slug, lesson_id):
    """Mark a lesson as complete"""
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        
        try:
            enrollment = Enrollment.objects.get(user=request.user, course=course)
            progress, created = LessonProgress.objects.get_or_create(
                enrollment=enrollment,
                lesson=lesson
            )
            
            if not progress.completed:
                from django.utils import timezone
                progress.completed = True
                progress.completed_at = timezone.now()
                progress.save()
                
                # Update overall course progress - avoid boolean filter
                all_lessons = list(course.lessons.all())
                total_lessons = len([l for l in all_lessons if l.is_published])
                
                all_progress = list(LessonProgress.objects.filter(enrollment=enrollment))
                completed_lessons = len([p for p in all_progress if p.completed])
                
                if total_lessons > 0:
                    enrollment.progress = (completed_lessons / total_lessons) * 100
                    enrollment.save()
                
                messages.success(request, f'Lesson "{lesson.title}" marked as complete!')
            else:
                messages.info(request, 'Lesson already completed.')
                
        except Enrollment.DoesNotExist:
            messages.error(request, 'You must enroll in this course first.')
    
    return redirect('lesson_view', course_slug=course_slug, lesson_id=lesson_id)
