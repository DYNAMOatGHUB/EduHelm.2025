from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.

@login_required
def home(request):
    """Dashboard home view with real user data"""
    from users.models import Profile, StudySession, StudySchedule
    
    # Get or create user profile
    profile, _ = Profile.objects.get_or_create(user=request.user)
    
    # Get study streak from profile
    study_streak = profile.study_streak or 0
    
    # Calculate weekly study time
    week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get all sessions from this week and filter inactive ones in Python
    all_week_sessions = list(StudySession.objects.filter(
        user=request.user, 
        start_time__gte=week_start
    ))
    weekly_sessions = [s for s in all_week_sessions if not s.is_active]
    weekly_study_minutes = sum(session.duration for session in weekly_sessions)
    weekly_study_hours = weekly_study_minutes / 60.0
    
    # Calculate weekly progress (assuming 20 hours/week goal)
    weekly_goal_hours = 20
    weekly_progress = min(100, int((weekly_study_hours / weekly_goal_hours) * 100))
    
    # Get today's scheduled events
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    
    upcoming_schedules = StudySchedule.objects.filter(
        user=request.user,
        is_active=True,
        scheduled_start__gte=today_start,
        scheduled_start__lte=today_end
    ).order_by('scheduled_start')[:5]
    
    context = {
        'study_streak': study_streak,
        'weekly_study_minutes': weekly_study_minutes,
        'weekly_study_hours': weekly_study_hours,
        'weekly_progress': weekly_progress,
        'upcoming_schedules': upcoming_schedules,
    }
    
    return render(request, 'sample/home.html', context)

