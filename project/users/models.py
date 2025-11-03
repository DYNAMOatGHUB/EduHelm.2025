from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # Additional profile fields
    bio = models.TextField(max_length=500, blank=True, help_text="Tell us about yourself")
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Study tracking
    study_streak = models.PositiveIntegerField(default=0, help_text="Current study streak in days")
    total_study_hours = models.FloatField(default=0.0)
    last_study_date = models.DateField(null=True, blank=True, help_text="Last date user studied")
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def update_study_streak(self):
        """Update study streak based on last study date"""
        today = timezone.now().date()
        
        if self.last_study_date is None:
            self.study_streak = 1
            self.last_study_date = today
        elif self.last_study_date == today:
            # Already studied today, no change
            pass
        elif self.last_study_date == today - timedelta(days=1):
            # Studied yesterday, increment streak
            self.study_streak += 1
            self.last_study_date = today
        else:
            # Streak broken
            self.study_streak = 1
            self.last_study_date = today
        
        self.save()
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    
    notes = models.TextField(blank=True, help_text="Session notes or reflections")
    is_active = models.BooleanField(default=True, help_text="Whether session is currently active")
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        course_name = self.course.title if self.course else "General Study"
        return f"{self.user.username} - {course_name} ({self.duration}min)"
    
    def end_session(self):
        """End the study session and calculate duration"""
        if self.is_active:
            self.end_time = timezone.now()
            self.is_active = False
            
            # Calculate duration in minutes
            duration_seconds = (self.end_time - self.start_time).total_seconds()
            self.duration = int(duration_seconds / 60)
            
            # Update user's total study hours
            profile = self.user.profile
            profile.total_study_hours += self.duration / 60.0
            profile.update_study_streak()
            profile.save()
            
            self.save()
    
    class Meta:
        verbose_name = 'Study Session'
        verbose_name_plural = 'Study Sessions'
        ordering = ['-start_time']


class StudyGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_goals')
    goal_type = models.CharField(max_length=10, choices=GOAL_TYPE_CHOICES, default='daily')
    target_minutes = models.PositiveIntegerField(help_text="Target study time in minutes")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()} Goal ({self.target_minutes}min)"
    
    def get_progress(self):
        """Calculate progress towards goal"""
        from datetime import datetime, timedelta
        
        now = timezone.now()
        
        if self.goal_type == 'daily':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.goal_type == 'weekly':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # monthly
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get sessions in the period
        sessions = StudySession.objects.filter(
            user=self.user,
            start_time__gte=start,
            is_active=False
        )
        
        total_minutes = sum(session.duration for session in sessions)
        percentage = min(100, int((total_minutes / self.target_minutes) * 100)) if self.target_minutes > 0 else 0
        
        return {
            'total_minutes': total_minutes,
            'target_minutes': self.target_minutes,
            'percentage': percentage,
            'remaining_minutes': max(0, self.target_minutes - total_minutes)
        }
    
    class Meta:
        verbose_name = 'Study Goal'
        verbose_name_plural = 'Study Goals'
        ordering = ['-created_at']


class StudySchedule(models.Model):
    """Scheduled study events or reminders (calendar entries)."""
    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_schedules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True, help_text='Optional duration in minutes')

    is_recurring = models.BooleanField(default=False)
    recurrence = models.CharField(max_length=10, choices=RECURRENCE_CHOICES, default='none')
    reminder_minutes_before = models.PositiveIntegerField(default=15, help_text='Minutes before start to remind')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.title} @ {self.scheduled_start.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'Study Schedule'
        verbose_name_plural = 'Study Schedules'
        ordering = ['scheduled_start']


class NoteCategory(models.Model):
    """Categories for organizing study notes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_categories')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#4CAF50', help_text="Hex color code for category")
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    class Meta:
        verbose_name = 'Note Category'
        verbose_name_plural = 'Note Categories'
        ordering = ['name']
        unique_together = ['user', 'name']


class StudyNote(models.Model):
    """User's study notes with rich text support"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_notes')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Note content (supports markdown)")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    is_pinned = models.BooleanField(default=False, help_text="Pin important notes to top")
    is_favorite = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def get_tags_list(self):
        """Return tags as a list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []
    
    class Meta:
        verbose_name = 'Study Note'
        verbose_name_plural = 'Study Notes'
        ordering = ['-is_pinned', '-updated_at']


class SharedResource(models.Model):
    """Shared learning resources (PDFs, videos, links, etc.)"""
    RESOURCE_TYPES = [
        ('pdf', 'PDF Document'),
        ('video', 'Video'),
        ('link', 'Web Link'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_resources')
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='resources')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='other')
    
    # For file uploads
    file = models.FileField(upload_to='study_resources/%Y/%m/', null=True, blank=True)
    
    # For external links
    url = models.URLField(max_length=500, blank=True)
    
    # Metadata
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    downloads = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    
    is_public = models.BooleanField(default=False, help_text="Make resource visible to other users")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_file_size_mb(self):
        """Return file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    class Meta:
        verbose_name = 'Shared Resource'
        verbose_name_plural = 'Shared Resources'
        ordering = ['-created_at']


# ============================================================================
# PHASE 5: COLLABORATIVE LEARNING MODELS
# ============================================================================

class StudyGroup(models.Model):
    """Study groups for collaborative learning"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    max_members = models.PositiveIntegerField(default=10, help_text="Maximum number of members allowed")
    is_private = models.BooleanField(default=False, help_text="Private groups require invitation to join")
    cover_image = models.ImageField(upload_to='group_covers/%Y/%m/', blank=True, null=True)
    
    # Associated course (optional)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='study_groups')
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def member_count(self):
        """Return current number of members"""
        return self.members.count()
    
    def is_full(self):
        """Check if group has reached max capacity"""
        return self.member_count() >= self.max_members
    
    def is_member(self, user):
        """Check if user is a member"""
        return self.members.filter(user=user).exists()
    
    def is_admin(self, user):
        """Check if user is an admin of the group"""
        return self.members.filter(user=user, role='admin').exists() or self.creator == user
    
    class Meta:
        verbose_name = 'Study Group'
        verbose_name_plural = 'Study Groups'
        ordering = ['-created_at']


class GroupMembership(models.Model):
    """Membership relationship between users and study groups"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"
    
    class Meta:
        verbose_name = 'Group Membership'
        verbose_name_plural = 'Group Memberships'
        unique_together = ['user', 'group']
        ordering = ['-joined_at']


class Discussion(models.Model):
    """Discussion threads within study groups"""
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Optional attachments
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False, help_text="Locked discussions cannot receive new replies")
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.group.name} - {self.title}"
    
    def reply_count(self):
        """Return number of replies"""
        return self.replies.count()
    
    def last_activity(self):
        """Return timestamp of last activity"""
        last_reply = self.replies.order_by('-created_at').first()
        if last_reply:
            return last_reply.created_at
        return self.created_at
    
    class Meta:
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'
        ordering = ['-is_pinned', '-updated_at']


class DiscussionReply(models.Model):
    """Replies to discussion threads"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_replies')
    content = models.TextField()
    
    # Threading support
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reply by {self.author.username} on {self.discussion.title}"
    
    class Meta:
        verbose_name = 'Discussion Reply'
        verbose_name_plural = 'Discussion Replies'
        ordering = ['created_at']


class PeerReview(models.Model):
    """Peer reviews for notes and resources"""
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Below Average'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]
    
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='peer_reviews_given')
    
    # Can review either a note or a resource
    note = models.ForeignKey(StudyNote, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    resource = models.ForeignKey(SharedResource, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
    
    rating = models.IntegerField(choices=RATING_CHOICES)
    feedback = models.TextField(help_text="Constructive feedback for the creator")
    
    # Helpful votes
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        target = self.note if self.note else self.resource
        return f"Review by {self.reviewer.username} - {self.rating}★"
    
    class Meta:
        verbose_name = 'Peer Review'
        verbose_name_plural = 'Peer Reviews'
        ordering = ['-created_at']


# ========== Achievement/Badge System ==========

class Badge(models.Model):
    """Achievement badges that users can earn"""
    BADGE_TYPES = [
        ('study', 'Study Milestone'),
        ('social', 'Social Engagement'),
        ('skill', 'Skill Mastery'),
        ('special', 'Special Achievement'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., fa-trophy)")
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='study')
    color = models.CharField(max_length=7, default='#FFD700', help_text="Hex color code")
    requirement = models.IntegerField(help_text="Requirement value (e.g., 100 hours, 50 notes)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        ordering = ['requirement']


class UserBadge(models.Model):
    """Badges earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
    
    class Meta:
        verbose_name = 'User Badge'
        verbose_name_plural = 'User Badges'
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']


# ========== Notification System ==========

class Notification(models.Model):
    """User notifications for various activities"""
    NOTIFICATION_TYPES = [
        ('discussion', 'New Discussion Reply'),
        ('group', 'Group Activity'),
        ('review', 'New Peer Review'),
        ('badge', 'Badge Earned'),
        ('goal', 'Goal Reminder'),
        ('system', 'System Announcement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, help_text="URL to related content")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def time_ago(self):
        """Return human-readable time since notification"""
        delta = timezone.now() - self.created_at
        
        if delta.days > 30:
            return f"{delta.days // 30} month{'s' if delta.days // 30 > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']


# ========== User Activity/Stats ==========

class UserActivity(models.Model):
    """Track user activities for the activity feed"""
    ACTIVITY_TYPES = [
        ('note_created', 'Created a Note'),
        ('resource_shared', 'Shared a Resource'),
        ('course_enrolled', 'Enrolled in Course'),
        ('group_joined', 'Joined Study Group'),
        ('discussion_posted', 'Posted Discussion'),
        ('goal_achieved', 'Achieved Study Goal'),
        ('badge_earned', 'Earned Badge'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=300)
    link = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_activity_type_display()}"
    
    def time_ago(self):
        """Return human-readable time since activity"""
        delta = timezone.now() - self.created_at
        
        if delta.days > 30:
            return f"{delta.days // 30} month{'s' if delta.days // 30 > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds > 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds > 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'
        ordering = ['-created_at']