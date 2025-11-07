import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.db import DatabaseError
from django.db.models import Sum, Count, Q
from datetime import datetime, timedelta
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import (
    StudySession, StudyGoal, NoteCategory, StudyNote, SharedResource,
    StudyGroup, GroupMembership, Discussion, DiscussionReply, PeerReview
)
from courses.models import Course
import os

logger = logging.getLogger(__name__)


def safe_queryset_count(qs):
    """Safely count documents, falling back when Djongo cannot translate COUNT."""
    try:
        return qs.count()
    except DatabaseError as exc:
        logger.warning("Count fallback for %s due to %s", qs.model.__name__, exc)
        try:
            return len(list(qs))
        except Exception as inner_exc:
            logger.error("Unable to evaluate queryset for %s: %s", qs.model.__name__, inner_exc)
            return 0


def get_inactive_sessions(user, order_by='-start_time', limit=None):
    """
    Safely retrieve inactive (completed) study sessions.
    Djongo has recursion issues with is_active=False, so we fetch all and filter in Python.
    """
    try:
        all_sessions = list(StudySession.objects.filter(user=user).order_by(order_by))
        inactive = [s for s in all_sessions if not s.is_active]
        return inactive[:limit] if limit else inactive
    except Exception as exc:
        logger.error("Failed to load inactive sessions for user %s: %s", user.username, exc)
        return []

def register(request):
    if request.method == "POST":                                                                            #This checks if the request is GET or POST (GET means "someone has just entered the register") and (POST means "someone has entered the register page and typed the details and since in the register.htlm we used POST .it returns back to the views.py file as POST along with the user typed data")
                                                                                                            #request.method = it is like either request.POST or request.GET
        form=UserRegisterForm(request.POST)                                                                 #Here is the actual validation procces occurs like username ,password validation
        if form.is_valid():
            user = form.save()                                                                              #If the form is valid data then here the form is saved in DB
            username=form.cleaned_data.get('username')                                                      #Here we get the username for the flash message and cleaned_data  gives the data in a python radable formate
            messages.success(request,f'Account created for {username}! You are now logged in.')             #messages.success stores the message temporarily and it is passed to the templates automatically .The actuall message printing work is done in the base.html
            login(request, user)                                                                            #Auto-login the user after successful registration
            return redirect('sample_home')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})



@login_required
def profile(request):
    # Ensure profile exists and gather high-level stats for dashboard view
    from .models import Profile

    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    notes_count = StudyNote.objects.filter(user=request.user).count()
    resources_count = SharedResource.objects.filter(user=request.user).count()
    groups_count = GroupMembership.objects.filter(user=request.user).count()
    
    # Fetch all goals and filter is_active in Python
    all_user_goals = list(StudyGoal.objects.filter(user=request.user))
    active_goals = [g for g in all_user_goals if g.is_active]
    goals_count = len(active_goals)
    
    badges_count = request.user.earned_badges.count() if hasattr(request.user, 'earned_badges') else 0

    recent_sessions = get_inactive_sessions(request.user, limit=5)
    recent_activity = request.user.activities.order_by('-created_at')[:5] if hasattr(request.user, 'activities') else []

    context = {
        'profile': profile_obj,
        'notes_count': notes_count,
        'resources_count': resources_count,
        'groups_count': groups_count,
        'goals_count': goals_count,
        'badges_count': badges_count,
        'recent_sessions': recent_sessions,
        'recent_activity': recent_activity,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    from .models import Profile

    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')

        messages.error(request, 'Please correct the highlighted errors and try again.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile_obj,
    }
    return render(request, 'users/profile_edit.html', context)


def logout_confirm(request):
    return render(request, 'users/logout_confirm.html')


# ========== Study Session Views ==========

@login_required
def study_dashboard(request):
    """Main study tracking dashboard with timer and analytics"""
    # Get active session - fetch all user sessions and filter in Python
    all_sessions = list(StudySession.objects.filter(user=request.user))
    active_sessions = [s for s in all_sessions if s.is_active]
    active_session = active_sessions[0] if active_sessions else None
    
    # Get user's active goals - fetch all goals and filter in Python
    all_goals = list(StudyGoal.objects.filter(user=request.user))
    goals = [g for g in all_goals if g.is_active]
    goals_data = [{'goal': goal, 'progress': goal.get_progress()} for goal in goals]
    
    # Get recent sessions (last 10)
    recent_sessions = get_inactive_sessions(request.user, limit=10)
    
    # Calculate today's study time
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    
    # Get all user sessions, filter today's inactive ones in Python
    all_user_sessions = list(StudySession.objects.filter(user=request.user, start_time__gte=today_start))
    today_sessions = [s for s in all_user_sessions if not s.is_active]
    today_minutes = sum(session.duration for session in today_sessions)
    
    # Get weekly stats
    week_start = timezone.now() - timedelta(days=timezone.now().weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    all_week_sessions = list(StudySession.objects.filter(user=request.user, start_time__gte=week_start))
    weekly_sessions = [s for s in all_week_sessions if not s.is_active]
    weekly_minutes = sum(session.duration for session in weekly_sessions)
    
    # Get all courses (no enrollment system in simplified version)
    enrolled_courses = Course.objects.all()
    
    # Ensure profile exists
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'active_session': active_session,
        'goals_data': goals_data,
        'recent_sessions': recent_sessions,
        'today_minutes': today_minutes,
        'weekly_minutes': weekly_minutes,
        'enrolled_courses': enrolled_courses,
        'profile': profile,
    }
    return render(request, 'users/study_dashboard.html', context)


@login_required
def start_session(request):
    """Start a new study session"""
    # Check if there's already an active session - fetch all and filter in Python
    all_sessions = list(StudySession.objects.filter(user=request.user))
    active_sessions = [s for s in all_sessions if s.is_active]
    active_session = active_sessions[0] if active_sessions else None
    
    if active_session:
        messages.warning(request, 'You already have an active study session!')
        return redirect('study_dashboard')
    
    # Get course if provided
    course_id = request.POST.get('course_id')
    course = None
    if course_id:
        course = get_object_or_404(Course, id=course_id)
    
    # Create new session
    session = StudySession.objects.create(
        user=request.user,
        course=course
    )
    
    messages.success(request, 'Study session started! Good luck! 📚')
    return redirect('study_dashboard')


@login_required
def end_session(request):
    """End the active study session"""
    # Fetch all sessions and filter active ones in Python
    all_sessions = list(StudySession.objects.filter(user=request.user))
    active_sessions = [s for s in all_sessions if s.is_active]
    active_session = active_sessions[0] if active_sessions else None
    
    if not active_session:
        messages.error(request, 'No active session found!')
        return redirect('study_dashboard')
    
    # Get notes if provided
    notes = request.POST.get('notes', '')
    if notes:
        active_session.notes = notes
    
    # End the session
    active_session.end_session()
    
    messages.success(request, f'Session ended! You studied for {active_session.duration} minutes. Great work! 🎉')
    return redirect('study_dashboard')


@login_required
def study_history(request):
    """View study session history with filters"""
    sessions = get_inactive_sessions(request.user)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    course_id = request.GET.get('course')
    
    # Apply filters in Python since we already have the list
    if date_from:
        from datetime import datetime
        date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
        sessions = [s for s in sessions if s.start_time.date() >= date_from_obj]
    if date_to:
        from datetime import datetime
        date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
        sessions = [s for s in sessions if s.start_time.date() <= date_to_obj]
    if course_id:
        sessions = [s for s in sessions if s.course_id == int(course_id)]
    
    # Calculate totals
    total_sessions = len(sessions)
    total_minutes = sum(session.duration for session in sessions)
    total_hours = total_minutes / 60.0
    
    # Group by course (manual aggregation)
    course_stats_dict = {}
    for session in sessions:
        course_title = session.course.title if session.course else "General Study"
        if course_title not in course_stats_dict:
            course_stats_dict[course_title] = {'total_time': 0, 'session_count': 0, 'course__title': course_title}
        course_stats_dict[course_title]['total_time'] += session.duration
        course_stats_dict[course_title]['session_count'] += 1
    
    course_stats = sorted(course_stats_dict.values(), key=lambda x: x['total_time'], reverse=True)
    
    # Get all courses (no enrollment system in simplified version)
    enrolled_courses = Course.objects.all()
    
    context = {
        'sessions': sessions,
        'total_sessions': total_sessions,
        'total_minutes': total_minutes,
        'total_hours': total_hours,
        'course_stats': course_stats,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, 'users/study_history.html', context)


@login_required
def schedule_list(request):
    """List scheduled study events (simple calendar/list view)."""
    from .models import StudySchedule

    # Get user's schedules
    schedules = StudySchedule.objects.filter(user=request.user, is_active=True)

    # Optional date range filter
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        try:
            from datetime import datetime
            df = datetime.strptime(date_from, '%Y-%m-%d')
            schedules = schedules.filter(scheduled_start__date__gte=df.date())
        except Exception:
            pass
    if date_to:
        try:
            from datetime import datetime
            dt = datetime.strptime(date_to, '%Y-%m-%d')
            schedules = schedules.filter(scheduled_start__date__lte=dt.date())
        except Exception:
            pass

    context = {
        'schedules': schedules,
    }
    return render(request, 'users/schedule_list.html', context)


@login_required
def schedule_create(request):
    """Create a new scheduled study event."""
    from .models import StudySchedule
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        start = request.POST.get('scheduled_start')
        end = request.POST.get('scheduled_end')
        duration = request.POST.get('duration_minutes')
        recurrence = request.POST.get('recurrence', 'none')
        reminder = request.POST.get('reminder_minutes_before', 15)

        try:
            from datetime import datetime
            scheduled_start = datetime.fromisoformat(start)
        except Exception:
            messages.error(request, 'Invalid start datetime format. Use YYYY-MM-DDTHH:MM')
            return redirect('study_schedule')

        scheduled_end = None
        if end:
            try:
                from datetime import datetime
                scheduled_end = datetime.fromisoformat(end)
            except Exception:
                scheduled_end = None

        schedule = StudySchedule.objects.create(
            user=request.user,
            title=title,
            description=description,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            duration_minutes=int(duration) if duration else None,
            is_recurring=(recurrence != 'none'),
            recurrence=recurrence,
            reminder_minutes_before=int(reminder) if reminder else 15,
        )

        messages.success(request, 'Scheduled event created successfully!')
        return redirect('study_schedule')

    # GET: render simple form
    return render(request, 'users/schedule_form.html')


@login_required
def schedule_delete(request, schedule_id):
    from .models import StudySchedule
    schedule = get_object_or_404(StudySchedule, id=schedule_id, user=request.user)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Scheduled event deleted.')
        return redirect('study_schedule')
    return render(request, 'users/schedule_delete_confirm.html', {'schedule': schedule})


@login_required
def schedule_events_api(request):
    """Return schedules as JSON events (for calendar widgets)."""
    from .models import StudySchedule
    schedules = StudySchedule.objects.filter(user=request.user, is_active=True)

    data = []
    for s in schedules:
        event = {
            'id': s.id,
            'title': s.title,
            'start': s.scheduled_start.isoformat(),
            'end': s.scheduled_end.isoformat() if s.scheduled_end else None,
            'allDay': False,
            'description': s.description,
            'duration_minutes': s.duration_minutes,
            'recurrence': s.recurrence,
            'reminder_minutes_before': s.reminder_minutes_before,
        }
        data.append(event)

    return JsonResponse(data, safe=False)


@login_required
def schedule_edit(request, schedule_id):
    """Edit an existing scheduled study event."""
    from .models import StudySchedule

    schedule = get_object_or_404(StudySchedule, id=schedule_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        start = request.POST.get('scheduled_start')
        end = request.POST.get('scheduled_end')
        duration = request.POST.get('duration_minutes')
        recurrence = request.POST.get('recurrence', 'none')
        reminder = request.POST.get('reminder_minutes_before', 15)

        try:
            from datetime import datetime
            schedule.scheduled_start = datetime.fromisoformat(start)
        except Exception:
            messages.error(request, 'Invalid start datetime format. Use YYYY-MM-DDTHH:MM')
            return redirect('study_schedule')

        if end:
            try:
                from datetime import datetime
                schedule.scheduled_end = datetime.fromisoformat(end)
            except Exception:
                schedule.scheduled_end = None

        schedule.title = title
        schedule.description = description
        schedule.duration_minutes = int(duration) if duration else None
        schedule.is_recurring = (recurrence != 'none')
        schedule.recurrence = recurrence
        schedule.reminder_minutes_before = int(reminder) if reminder else 15
        schedule.save()

        messages.success(request, 'Scheduled event updated successfully!')
        return redirect('study_schedule')

    # GET: render form with existing schedule
    context = {'schedule': schedule}
    return render(request, 'users/schedule_form.html', context)


@login_required
def schedule_calendar(request):
    """Render calendar view powered by FullCalendar (client fetches /api/schedule/events/)."""
    return render(request, 'users/schedule_calendar.html')


@login_required
def study_analytics(request):
    """Advanced analytics and visualizations"""
    import json
    
    # Get all completed sessions
    all_sessions = get_inactive_sessions(request.user)
    
    # Last 30 days data for chart
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_sessions = [s for s in all_sessions if s.start_time >= thirty_days_ago]
    
    # Daily breakdown for last 30 days
    daily_data = []
    for i in range(30):
        date = (timezone.now() - timedelta(days=i)).date()
        day_start = timezone.make_aware(datetime.combine(date, datetime.min.time()))
        day_end = timezone.make_aware(datetime.combine(date, datetime.max.time()))
        
        day_sessions = [s for s in recent_sessions if day_start <= s.start_time <= day_end]
        day_minutes = sum(session.duration for session in day_sessions)
        
        daily_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'minutes': day_minutes
        })
    
    daily_data.reverse()
    
    # Course breakdown - manually aggregate in Python
    from collections import defaultdict
    course_stats = defaultdict(lambda: {'total_minutes': 0, 'session_count': 0})
    
    for session in all_sessions:
        course_title = session.course.title if session.course else 'No Course'
        course_stats[course_title]['total_minutes'] += session.duration
        course_stats[course_title]['session_count'] += 1
    
    # Convert to list and sort by total_minutes
    course_breakdown = [
        {'course__title': title, **stats}
        for title, stats in sorted(course_stats.items(), key=lambda x: x[1]['total_minutes'], reverse=True)[:5]
    ]
    
    # Time of day analysis - manually aggregate in Python
    morning_minutes = sum(s.duration for s in all_sessions if s.start_time.hour < 12)
    afternoon_minutes = sum(s.duration for s in all_sessions if 12 <= s.start_time.hour < 18)
    evening_minutes = sum(s.duration for s in all_sessions if s.start_time.hour >= 18)
    
    # Overall stats
    total_sessions = len(all_sessions)
    total_minutes = sum(session.duration for session in all_sessions)
    avg_session = total_minutes / total_sessions if total_sessions > 0 else 0
    
    # Ensure profile exists
    from .models import Profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'daily_data': json.dumps(daily_data),
        'course_breakdown': json.dumps(course_breakdown),
        'morning_minutes': morning_minutes,
        'afternoon_minutes': afternoon_minutes,
        'evening_minutes': evening_minutes,
        'total_sessions': total_sessions,
        'total_hours': total_minutes / 60.0,
        'avg_session_minutes': avg_session,
        'profile': profile,
    }
    return render(request, 'users/study_analytics.html', context)


@login_required
def manage_goals(request):
    """Manage study goals"""
    if request.method == 'POST':
        goal_type = request.POST.get('goal_type')
        target_minutes = request.POST.get('target_minutes')
        
        # Deactivate existing goal of same type - fetch all and filter in Python
        try:
            all_goals = list(StudyGoal.objects.filter(user=request.user, goal_type=goal_type))
            existing_goals = [g for g in all_goals if g.is_active]
            for goal in existing_goals:
                goal.is_active = False
                goal.save()
        except Exception as exc:
            logger.warning("Could not deactivate old goals: %s", exc)
        
        # Create new goal
        StudyGoal.objects.create(
            user=request.user,
            goal_type=goal_type,
            target_minutes=int(target_minutes)
        )
        
        messages.success(request, f'{goal_type.capitalize()} goal set successfully!')
        return redirect('study_dashboard')
    
    # Fetch all goals and filter active ones in Python
    all_goals = list(StudyGoal.objects.filter(user=request.user))
    goals = [g for g in all_goals if g.is_active]
    return render(request, 'users/manage_goals.html', {'goals': goals})


@login_required
def delete_goal(request, goal_id):
    """Delete a study goal"""
    goal = get_object_or_404(StudyGoal, id=goal_id, user=request.user)
    goal.delete()
    messages.success(request, 'Goal deleted successfully!')
    return redirect('study_dashboard')


# ========== Notes & Resources Views ==========

@login_required
def notes_list(request):
    """List all user's notes with filtering"""
    notes = StudyNote.objects.filter(user=request.user)
    
    # Filters
    category_id = request.GET.get('category')
    course_id = request.GET.get('course')
    search = request.GET.get('search')
    filter_type = request.GET.get('filter', 'all')
    
    if category_id:
        notes = notes.filter(category_id=category_id)
    if course_id:
        notes = notes.filter(course_id=course_id)
    if search:
        notes = notes.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(tags__icontains=search))
    
    if filter_type == 'pinned':
        # Fetch all notes then filter is_pinned in Python
        all_notes = list(notes)
        notes = [n for n in all_notes if n.is_pinned]
        notes_count = len(notes)
    elif filter_type == 'favorites':
        # Fetch all notes then filter is_favorite in Python
        all_notes = list(notes)
        notes = [n for n in all_notes if n.is_favorite]
        notes_count = len(notes)
    else:
        notes_count = notes.count()
    
    # Get categories and courses for filters
    categories = NoteCategory.objects.filter(user=request.user)
    courses = Course.objects.all()
    
    context = {
        'notes': notes,
        'categories': categories,
        'courses': courses,
        'total_notes': notes_count,
    }
    return render(request, 'users/notes_list.html', context)


@login_required
def note_create(request):
    """Create a new note"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')
        category_id = request.POST.get('category')
        course_id = request.POST.get('course')
        is_pinned = request.POST.get('is_pinned') == 'on'
        is_favorite = request.POST.get('is_favorite') == 'on'
        
        note = StudyNote.objects.create(
            user=request.user,
            title=title,
            content=content,
            tags=tags,
            is_pinned=is_pinned,
            is_favorite=is_favorite
        )
        
        if category_id:
            note.category_id = category_id
        if course_id:
            note.course_id = course_id
        
        note.save()
        
        messages.success(request, 'Note created successfully!')
        return redirect('note_detail', note_id=note.id)
    
    categories = NoteCategory.objects.filter(user=request.user)
    courses = Course.objects.all()
    
    context = {
        'categories': categories,
        'courses': courses,
    }
    return render(request, 'users/note_form.html', context)


@login_required
def note_detail(request, note_id):
    """View a single note"""
    note = get_object_or_404(StudyNote, id=note_id, user=request.user)
    
    context = {
        'note': note,
    }
    return render(request, 'users/note_detail.html', context)


@login_required
def note_edit(request, note_id):
    """Edit an existing note"""
    note = get_object_or_404(StudyNote, id=note_id, user=request.user)
    
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.tags = request.POST.get('tags', '')
        note.is_pinned = request.POST.get('is_pinned') == 'on'
        note.is_favorite = request.POST.get('is_favorite') == 'on'
        
        category_id = request.POST.get('category')
        course_id = request.POST.get('course')
        
        note.category_id = category_id if category_id else None
        note.course_id = course_id if course_id else None
        
        note.save()
        
        messages.success(request, 'Note updated successfully!')
        return redirect('note_detail', note_id=note.id)
    
    categories = NoteCategory.objects.filter(user=request.user)
    courses = Course.objects.all()
    
    context = {
        'note': note,
        'categories': categories,
        'courses': courses,
        'is_edit': True,
    }
    return render(request, 'users/note_form.html', context)


@login_required
def note_delete(request, note_id):
    """Delete a note"""
    note = get_object_or_404(StudyNote, id=note_id, user=request.user)
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('notes_list')


@login_required
def toggle_note_pin(request, note_id):
    """Toggle note pin status"""
    note = get_object_or_404(StudyNote, id=note_id, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('notes_list')


@login_required
def toggle_note_favorite(request, note_id):
    """Toggle note favorite status"""
    note = get_object_or_404(StudyNote, id=note_id, user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect('notes_list')


@login_required
def categories_manage(request):
    """Manage note categories"""
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#4CAF50')
        icon = request.POST.get('icon', '')
        description = request.POST.get('description', '')
        
        NoteCategory.objects.create(
            user=request.user,
            name=name,
            color=color,
            icon=icon,
            description=description
        )
        
        messages.success(request, f'Category "{name}" created successfully!')
        return redirect('categories_manage')
    
    categories = NoteCategory.objects.filter(user=request.user)
    
    context = {
        'categories': categories,
    }
    return render(request, 'users/categories_manage.html', context)


@login_required
def category_delete(request, category_id):
    """Delete a category"""
    category = get_object_or_404(NoteCategory, id=category_id, user=request.user)
    category.delete()
    messages.success(request, 'Category deleted successfully!')
    return redirect('categories_manage')


@login_required
def resources_library(request):
    """View all resources"""
    # User's own resources
    my_resources = SharedResource.objects.filter(user=request.user)
    
    # Public resources from other users - fetch all then filter is_public in Python
    all_resources = list(SharedResource.objects.exclude(user=request.user))
    public_resources_list = [r for r in all_resources if r.is_public]
    
    # Filters
    resource_type = request.GET.get('type')
    course_id = request.GET.get('course')
    search = request.GET.get('search')
    
    if resource_type:
        my_resources = my_resources.filter(resource_type=resource_type)
        public_resources_list = [r for r in public_resources_list if r.resource_type == resource_type]
    
    if course_id:
        my_resources = my_resources.filter(course_id=course_id)
        public_resources_list = [r for r in public_resources_list if str(r.course_id) == course_id]
    
    if search:
        my_resources = my_resources.filter(Q(title__icontains=search) | Q(description__icontains=search))
        search_lower = search.lower()
        public_resources_list = [r for r in public_resources_list 
                                 if search_lower in r.title.lower() or search_lower in (r.description or '').lower()]
    
    courses = Course.objects.all()
    
    context = {
        'my_resources': my_resources,
        'public_resources': public_resources_list,
        'public_resources_count': len(public_resources_list),
        'my_resources_count': my_resources.count(),
        'courses': courses,
        'resource_types': SharedResource.RESOURCE_TYPES,
    }
    return render(request, 'users/resources_library.html', context)


@login_required
def resource_upload(request):
    """Upload a new resource"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        resource_type = request.POST.get('resource_type')
        url = request.POST.get('url', '')
        course_id = request.POST.get('course')
        is_public = request.POST.get('is_public') == 'on'
        
        resource = SharedResource.objects.create(
            user=request.user,
            title=title,
            description=description,
            resource_type=resource_type,
            url=url,
            is_public=is_public
        )
        
        if course_id:
            resource.course_id = course_id
        
        # Handle file upload
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            resource.file = uploaded_file
            resource.file_size = uploaded_file.size
        
        resource.save()
        
        messages.success(request, 'Resource uploaded successfully!')
        return redirect('resources_library')
    
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
        'resource_types': SharedResource.RESOURCE_TYPES,
    }
    return render(request, 'users/resource_upload.html', context)


@login_required
def resource_view(request, resource_id):
    """View a resource and increment view count"""
    resource = get_object_or_404(SharedResource, id=resource_id)
    
    # Check permissions
    if not resource.is_public and resource.user != request.user:
        messages.error(request, 'You do not have permission to view this resource.')
        return redirect('resources_library')
    
    # Increment views
    resource.views += 1
    resource.save()
    
    context = {
        'resource': resource,
    }
    return render(request, 'users/resource_view.html', context)


@login_required
def resource_delete(request, resource_id):
    """Delete a resource"""
    resource = get_object_or_404(SharedResource, id=resource_id, user=request.user)
    
    # Delete file if exists
    if resource.file:
        if os.path.exists(resource.file.path):
            os.remove(resource.file.path)
    
    resource.delete()
    messages.success(request, 'Resource deleted successfully!')
    return redirect('resources_library')


# ============================================================================
# PHASE 5: COLLABORATIVE LEARNING VIEWS
# ============================================================================

@login_required
def groups_list(request):
    """List all study groups"""
    # Get user's groups
    my_groups = StudyGroup.objects.filter(members__user=request.user).distinct()
    
    # Get public groups user is not a member of - fetch all and filter is_private in Python
    all_other_groups = list(StudyGroup.objects.exclude(members__user=request.user))
    public_groups = [g for g in all_other_groups if not g.is_private]
    
    # Apply filters
    search = request.GET.get('search', '')
    course_id = request.GET.get('course', '')
    
    if search:
        my_groups = my_groups.filter(Q(name__icontains=search) | Q(description__icontains=search))
        search_lower = search.lower()
        public_groups = [g for g in public_groups 
                        if search_lower in g.name.lower() or search_lower in (g.description or '').lower()]
    
    if course_id:
        my_groups = my_groups.filter(course_id=course_id)
        public_groups = [g for g in public_groups if str(g.course_id) == course_id]
    
    # Fetch all courses and filter is_published in Python
    all_courses = list(Course.objects.all())
    courses = [c for c in all_courses if c.is_published]
    
    context = {
        'my_groups': my_groups,
        'public_groups': public_groups,
        'courses': courses,
        'total_groups': my_groups.count(),
    }
    return render(request, 'users/groups_list.html', context)


@login_required
def group_create(request):
    """Create a new study group"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        max_members = request.POST.get('max_members', 10)
        is_private = request.POST.get('is_private') == 'on'
        course_id = request.POST.get('course')
        
        group = StudyGroup.objects.create(
            name=name,
            description=description,
            creator=request.user,
            max_members=int(max_members),
            is_private=is_private
        )
        
        if course_id:
            group.course_id = course_id
        
        # Handle cover image
        if 'cover_image' in request.FILES:
            group.cover_image = request.FILES['cover_image']
        
        group.save()
        
        # Auto-join creator as admin
        GroupMembership.objects.create(
            user=request.user,
            group=group,
            role='admin'
        )
        
        messages.success(request, f'Study group "{group.name}" created successfully!')
        return redirect('group_detail', group_id=group.id)
    
    # Fetch all courses and filter is_published in Python
    all_courses = list(Course.objects.all())
    courses = [c for c in all_courses if c.is_published]
    context = {'courses': courses}
    return render(request, 'users/group_create.html', context)


@login_required
def group_detail(request, group_id):
    """View study group details"""
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check if user is a member
    is_member = group.is_member(request.user)
    is_admin = group.is_admin(request.user)
    
    # For private groups, only members can view
    if group.is_private and not is_member:
        messages.error(request, 'This is a private group.')
        return redirect('groups_list')
    
    # Get recent discussions
    discussions = group.discussions.all()[:10]
    
    # Get members
    members = group.members.select_related('user').all()
    
    context = {
        'group': group,
        'is_member': is_member,
        'is_admin': is_admin,
        'discussions': discussions,
        'members': members,
    }
    return render(request, 'users/group_detail.html', context)


@login_required
def group_join(request, group_id):
    """Join a study group"""
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check if already a member
    if group.is_member(request.user):
        messages.info(request, 'You are already a member of this group.')
        return redirect('group_detail', group_id=group.id)
    
    # Check if group is full
    if group.is_full():
        messages.error(request, 'This group is full.')
        return redirect('groups_list')
    
    # Join the group
    GroupMembership.objects.create(
        user=request.user,
        group=group,
        role='member'
    )
    
    messages.success(request, f'You have joined "{group.name}"!')
    return redirect('group_detail', group_id=group.id)


@login_required
def group_leave(request, group_id):
    """Leave a study group"""
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Can't leave if you're the creator
    if group.creator == request.user:
        messages.error(request, 'Group creators cannot leave. Transfer ownership or delete the group.')
        return redirect('group_detail', group_id=group.id)
    
    # Remove membership
    GroupMembership.objects.filter(user=request.user, group=group).delete()
    
    messages.success(request, f'You have left "{group.name}".')
    return redirect('groups_list')


@login_required
def group_delete(request, group_id):
    """Delete a study group (creator only)"""
    group = get_object_or_404(StudyGroup, id=group_id, creator=request.user)
    
    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f'Group "{group_name}" deleted successfully.')
        return redirect('groups_list')
    
    return redirect('group_detail', group_id=group.id)


@login_required
def discussion_list(request, group_id):
    """List discussions in a group"""
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check membership
    if not group.is_member(request.user):
        messages.error(request, 'You must be a member to view discussions.')
        return redirect('group_detail', group_id=group.id)
    
    discussions = group.discussions.all()
    
    context = {
        'group': group,
        'discussions': discussions,
        'is_admin': group.is_admin(request.user),
    }
    return render(request, 'users/discussion_list.html', context)


@login_required
def discussion_create(request, group_id):
    """Create a new discussion"""
    group = get_object_or_404(StudyGroup, id=group_id)
    
    # Check membership
    if not group.is_member(request.user):
        messages.error(request, 'You must be a member to create discussions.')
        return redirect('group_detail', group_id=group.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        discussion = Discussion.objects.create(
            group=group,
            author=request.user,
            title=title,
            content=content
        )
        
        messages.success(request, 'Discussion created successfully!')
        return redirect('discussion_detail', discussion_id=discussion.id)
    
    context = {'group': group}
    return render(request, 'users/discussion_create.html', context)


@login_required
def discussion_detail(request, discussion_id):
    """View discussion and replies"""
    discussion = get_object_or_404(Discussion, id=discussion_id)
    group = discussion.group
    
    # Check membership
    if not group.is_member(request.user):
        messages.error(request, 'You must be a member to view this discussion.')
        return redirect('groups_list')
    
    # Handle reply submission
    if request.method == 'POST' and not discussion.is_locked:
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        reply = DiscussionReply.objects.create(
            discussion=discussion,
            author=request.user,
            content=content
        )
        
        if parent_id:
            reply.parent_id = parent_id
            reply.save()
        
        messages.success(request, 'Reply added successfully!')
        return redirect('discussion_detail', discussion_id=discussion.id)
    
    replies = discussion.replies.filter(parent=None).prefetch_related('children')
    
    context = {
        'discussion': discussion,
        'group': group,
        'replies': replies,
        'is_admin': group.is_admin(request.user),
    }
    return render(request, 'users/discussion_detail.html', context)


@login_required
def discussion_delete(request, discussion_id):
    """Delete a discussion (author or admin only)"""
    discussion = get_object_or_404(Discussion, id=discussion_id)
    group = discussion.group
    
    # Check permissions
    if discussion.author != request.user and not group.is_admin(request.user):
        messages.error(request, 'You do not have permission to delete this discussion.')
        return redirect('discussion_detail', discussion_id=discussion.id)
    
    if request.method == 'POST':
        group_id = group.id
        discussion.delete()
        messages.success(request, 'Discussion deleted successfully.')
        return redirect('discussion_list', group_id=group_id)
    
    return redirect('discussion_detail', discussion_id=discussion.id)


@login_required
def add_review(request, target_type, target_id):
    """Add a peer review to a note or resource"""
    if target_type == 'note':
        target = get_object_or_404(StudyNote, id=target_id)
        if target.user == request.user:
            messages.error(request, 'You cannot review your own note.')
            return redirect('note_detail', note_id=target_id)
    else:
        target = get_object_or_404(SharedResource, id=target_id)
        if target.user == request.user:
            messages.error(request, 'You cannot review your own resource.')
            return redirect('resource_view', resource_id=target_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        
        review = PeerReview.objects.create(
            reviewer=request.user,
            rating=int(rating),
            feedback=feedback
        )
        
        if target_type == 'note':
            review.note = target
        else:
            review.resource = target
        
        review.save()
        
        messages.success(request, 'Review submitted successfully!')
        
        if target_type == 'note':
            return redirect('note_detail', note_id=target_id)
        else:
            return redirect('resource_view', resource_id=target_id)
    
    context = {
        'target': target,
        'target_type': target_type,
    }
    return render(request, 'users/add_review.html', context)


# ============================================================================
# SURPRISE FEATURES: NOTIFICATIONS & BADGES
# ============================================================================

@login_required
def get_notifications(request):
    """Get user notifications (AJAX endpoint)"""
    from .models import Notification
    
    notifications = list(Notification.objects.filter(user=request.user).order_by('-created_at')[:20])
    
    # Count unread notifications in Python
    unread_count = len([n for n in notifications if not n.is_read])
    
    data = {
        'notifications': [
            {
                'id': str(n.id),
                'type': n.notification_type,
                'title': n.title,
                'message': n.message,
                'link': n.link,
                'is_read': n.is_read,
                'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'time_ago': n.time_ago(),
            }
            for n in notifications
        ],
        'unread_count': unread_count
    }
    
    return JsonResponse(data)


@login_required
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    from .models import Notification
    
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.mark_as_read()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    # Redirect to link if exists
    if notification.link:
        return redirect(notification.link)
    
    return redirect('profile')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from .models import Notification
    
    # Fetch all unread notifications and mark them read in Python
    all_notifications = list(Notification.objects.filter(user=request.user))
    unread_notifications = [n for n in all_notifications if not n.is_read]
    for n in unread_notifications:
        n.is_read = True
        n.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    messages.success(request, 'All notifications marked as read!')
    return redirect('profile')


@login_required
def get_user_badges(request):
    """Get user's earned badges"""
    from .models import UserBadge, Badge
    
    # Get earned badges
    earned_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
    
    # Get all available badges - fetch all and filter is_active in Python
    all_badges_list = list(Badge.objects.all())
    all_badges = [b for b in all_badges_list if b.is_active]
    
    badge_data = []
    for badge in all_badges:
        user_badge = earned_badges.filter(badge=badge).first()
        badge_data.append({
            'id': str(badge.id),
            'name': badge.name,
            'description': badge.description,
            'icon': badge.icon,
            'color': badge.color,
            'badge_type': badge.badge_type,
            'requirement': badge.requirement,
            'earned': user_badge is not None,
            'earned_at': user_badge.earned_at.strftime('%Y-%m-%d') if user_badge else None,
        })
    
    data = {
        'badges': badge_data,
        'total_earned': earned_badges.count(),
        'total_available': len(all_badges),
    }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(data)
    
    return render(request, 'users/badges.html', data)


@login_required
def check_badge_eligibility(request):
    """Check and auto-award eligible badges"""
    from .models import Badge, UserBadge, Notification, Profile
    from django.db.models import Sum, Count
    
    profile = Profile.objects.get(user=request.user)
    newly_earned = []
    
    # Get all active badges - fetch all and filter in Python
    all_badges_list = list(Badge.objects.all())
    badges = [b for b in all_badges_list if b.is_active]
    
    for badge in badges:
        # Skip if already earned
        if UserBadge.objects.filter(user=request.user, badge=badge).exists():
            continue
        
        earned = False
        
        # Check study badges
        if badge.badge_type == 'study':
            total_hours = profile.total_study_hours or 0
            
            if 'First Steps' in badge.name and total_hours >= 1:
                earned = True
            elif '10 Hour Hero' in badge.name and total_hours >= 10:
                earned = True
            elif 'Century Scholar' in badge.name and total_hours >= 100:
                earned = True
            elif '7 Day Streak' in badge.name and (profile.study_streak or 0) >= 7:
                earned = True
            elif '30 Day Champion' in badge.name and (profile.study_streak or 0) >= 30:
                earned = True
        
        # Check social badges
        elif badge.badge_type == 'social':
            if 'Team Player' in badge.name:
                group_count = GroupMembership.objects.filter(user=request.user).count()
                if group_count >= 1:
                    earned = True
            elif 'Discussion Starter' in badge.name:
                discussion_count = Discussion.objects.filter(author=request.user).count()
                if discussion_count >= 10:
                    earned = True
            elif 'Helpful Peer' in badge.name:
                review_count = PeerReview.objects.filter(reviewer=request.user).count()
                if review_count >= 25:
                    earned = True
        
        # Check skill badges
        elif badge.badge_type == 'skill':
            if 'Note Taker' in badge.name:
                note_count = StudyNote.objects.filter(user=request.user).count()
                if note_count >= 10:
                    earned = True
            elif 'Resource Master' in badge.name:
                resource_count = SharedResource.objects.filter(user=request.user).count()
                if resource_count >= 20:
                    earned = True
            elif 'Course Enthusiast' in badge.name:
                # No enrollment system in simplified version - award based on lesson progress
                from courses.models import LessonProgress
                completed_lessons = LessonProgress.objects.filter(
                    user_link=request.user, 
                    is_completed=True
                ).count()
                if completed_lessons >= 5:
                    earned = True
        
        # Check special badges
        elif badge.badge_type == 'special':
            if 'Master Student' in badge.name:
                earned_count = UserBadge.objects.filter(user=request.user).count()
                if earned_count >= 10:
                    earned = True
        
        # Award badge if earned
        if earned:
            UserBadge.objects.create(user=request.user, badge=badge)
            
            # Create notification
            Notification.objects.create(
                user=request.user,
                notification_type='badge',
                title=f'🏆 Badge Earned: {badge.name}',
                message=badge.description,
                link='/profile/'
            )
            
            newly_earned.append(badge)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'newly_earned': [
                {
                    'name': b.name,
                    'icon': b.icon,
                    'color': b.color,
                    'description': b.description
                }
                for b in newly_earned
            ],
            'count': len(newly_earned)
        })
    
    if newly_earned:
        messages.success(request, f'Congratulations! You earned {len(newly_earned)} new badge(s)!')
    
    return redirect('profile')


@login_required
def get_activity_feed(request):
    """Get user's recent activity"""
    from .models import UserActivity
    
    activities = UserActivity.objects.filter(user=request.user).order_by('-created_at')[:20]
    
    data = {
        'activities': [
            {
                'id': str(a.id),
                'activity_type': a.activity_type,
                'description': a.description,
                'link': a.link,
                'created_at': a.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'time_ago': a.time_ago(),
            }
            for a in activities
        ]
    }
    
    return JsonResponse(data)
