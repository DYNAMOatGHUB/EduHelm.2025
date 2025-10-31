from django.contrib import admin
from .models import (
    Profile, StudySession, StudyGoal, NoteCategory, StudyNote, SharedResource,
    StudyGroup, GroupMembership, Discussion, DiscussionReply, PeerReview,
    Badge, UserBadge, Notification, UserActivity
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'study_streak', 'total_study_hours', 'last_study_date', 'updated_at']
    list_filter = ['location', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'bio', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'image')
        }),
        ('Personal Details', {
            'fields': ('bio', 'phone_number', 'location', 'date_of_birth')
        }),
        ('Study Statistics', {
            'fields': ('study_streak', 'total_study_hours', 'last_study_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'start_time', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'start_time', 'course']
    search_fields = ['user__username', 'notes', 'course__title']
    readonly_fields = ['created_at', 'duration']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Session Info', {
            'fields': ('user', 'course', 'is_active')
        }),
        ('Time Tracking', {
            'fields': ('start_time', 'end_time', 'duration')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['end_selected_sessions']
    
    def end_selected_sessions(self, request, queryset):
        """End multiple active sessions"""
        count = 0
        for session in queryset.filter(is_active=True):
            session.end_session()
            count += 1
        self.message_user(request, f'{count} session(s) ended successfully.')
    end_selected_sessions.short_description = "End selected active sessions"


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_type', 'target_minutes', 'is_active', 'created_at']
    list_filter = ['goal_type', 'is_active', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('user', 'goal_type', 'target_minutes', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(NoteCategory)
class NoteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'icon', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'user__username', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Category Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Appearance', {
            'fields': ('color', 'icon')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudyNote)
class StudyNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'course', 'category', 'is_pinned', 'is_favorite', 'created_at', 'updated_at']
    list_filter = ['is_pinned', 'is_favorite', 'category', 'course', 'created_at']
    search_fields = ['title', 'content', 'tags', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Note Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Organization', {
            'fields': ('course', 'category', 'tags')
        }),
        ('Flags', {
            'fields': ('is_pinned', 'is_favorite')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_pinned', 'mark_as_favorite']
    
    def mark_as_pinned(self, request, queryset):
        count = queryset.update(is_pinned=True)
        self.message_user(request, f'{count} note(s) pinned successfully.')
    mark_as_pinned.short_description = "Pin selected notes"
    
    def mark_as_favorite(self, request, queryset):
        count = queryset.update(is_favorite=True)
        self.message_user(request, f'{count} note(s) marked as favorite.')
    mark_as_favorite.short_description = "Mark as favorite"


@admin.register(SharedResource)
class SharedResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'resource_type', 'course', 'is_public', 'downloads', 'views', 'created_at']
    list_filter = ['resource_type', 'is_public', 'created_at', 'course']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'downloads', 'views', 'file_size']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Resource Information', {
            'fields': ('user', 'title', 'description', 'resource_type')
        }),
        ('Content', {
            'fields': ('file', 'url')
        }),
        ('Organization', {
            'fields': ('course', 'is_public')
        }),
        ('Statistics', {
            'fields': ('file_size', 'downloads', 'views')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_public', 'make_private']
    
    def make_public(self, request, queryset):
        count = queryset.update(is_public=True)
        self.message_user(request, f'{count} resource(s) made public.')
    make_public.short_description = "Make selected resources public"
    
    def make_private(self, request, queryset):
        count = queryset.update(is_public=False)
        self.message_user(request, f'{count} resource(s) made private.')
    make_private.short_description = "Make selected resources private"


# ============================================================================
# PHASE 5: COLLABORATIVE LEARNING ADMIN
# ============================================================================

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'course', 'member_count', 'max_members', 'is_private', 'created_at']
    list_filter = ['is_private', 'course', 'created_at']
    search_fields = ['name', 'description', 'creator__username']
    readonly_fields = ['created_at', 'updated_at', 'member_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Group Information', {
            'fields': ('name', 'description', 'creator')
        }),
        ('Settings', {
            'fields': ('max_members', 'is_private', 'cover_image')
        }),
        ('Association', {
            'fields': ('course',)
        }),
        ('Statistics', {
            'fields': ('member_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at']
    list_filter = ['role', 'joined_at', 'group']
    search_fields = ['user__username', 'group__name']
    readonly_fields = ['joined_at']
    date_hierarchy = 'joined_at'
    
    fieldsets = (
        ('Membership Information', {
            'fields': ('user', 'group', 'role')
        }),
        ('Metadata', {
            'fields': ('joined_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['promote_to_admin', 'promote_to_moderator', 'demote_to_member']
    
    def promote_to_admin(self, request, queryset):
        count = queryset.update(role='admin')
        self.message_user(request, f'{count} member(s) promoted to admin.')
    promote_to_admin.short_description = "Promote to Admin"
    
    def promote_to_moderator(self, request, queryset):
        count = queryset.update(role='moderator')
        self.message_user(request, f'{count} member(s) promoted to moderator.')
    promote_to_moderator.short_description = "Promote to Moderator"
    
    def demote_to_member(self, request, queryset):
        count = queryset.update(role='member')
        self.message_user(request, f'{count} member(s) demoted to member.')
    demote_to_member.short_description = "Demote to Member"


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'author', 'reply_count', 'is_pinned', 'is_locked', 'created_at']
    list_filter = ['is_pinned', 'is_locked', 'group', 'created_at']
    search_fields = ['title', 'content', 'author__username', 'group__name']
    readonly_fields = ['created_at', 'updated_at', 'reply_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Discussion Information', {
            'fields': ('group', 'author', 'title', 'content')
        }),
        ('Settings', {
            'fields': ('is_pinned', 'is_locked')
        }),
        ('Statistics', {
            'fields': ('reply_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['pin_discussions', 'unpin_discussions', 'lock_discussions', 'unlock_discussions']
    
    def pin_discussions(self, request, queryset):
        count = queryset.update(is_pinned=True)
        self.message_user(request, f'{count} discussion(s) pinned.')
    pin_discussions.short_description = "Pin selected discussions"
    
    def unpin_discussions(self, request, queryset):
        count = queryset.update(is_pinned=False)
        self.message_user(request, f'{count} discussion(s) unpinned.')
    unpin_discussions.short_description = "Unpin selected discussions"
    
    def lock_discussions(self, request, queryset):
        count = queryset.update(is_locked=True)
        self.message_user(request, f'{count} discussion(s) locked.')
    lock_discussions.short_description = "Lock selected discussions"
    
    def unlock_discussions(self, request, queryset):
        count = queryset.update(is_locked=False)
        self.message_user(request, f'{count} discussion(s) unlocked.')
    unlock_discussions.short_description = "Unlock selected discussions"


@admin.register(DiscussionReply)
class DiscussionReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'author', 'created_at', 'has_parent']
    list_filter = ['created_at', 'discussion']
    search_fields = ['content', 'author__username', 'discussion__title']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def has_parent(self, obj):
        return obj.parent is not None
    has_parent.boolean = True
    has_parent.short_description = "Is Reply"
    
    fieldsets = (
        ('Reply Information', {
            'fields': ('discussion', 'author', 'content')
        }),
        ('Threading', {
            'fields': ('parent',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PeerReview)
class PeerReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'rating', 'target_type', 'helpful_count', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['feedback', 'reviewer__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def target_type(self, obj):
        if obj.note:
            return f"Note: {obj.note.title}"
        elif obj.resource:
            return f"Resource: {obj.resource.title}"
        return "Unknown"
    target_type.short_description = "Target"
    
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'rating', 'feedback')
        }),
        ('Target', {
            'fields': ('note', 'resource')
        }),
        ('Statistics', {
            'fields': ('helpful_count',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['reset_helpful_count']
    
    def reset_helpful_count(self, request, queryset):
        count = queryset.update(helpful_count=0)
        self.message_user(request, f'Reset helpful count for {count} review(s).')
    reset_helpful_count.short_description = "Reset helpful count"


# ========== Achievement/Badge Admin ==========

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'requirement', 'color', 'is_active', 'created_at']
    list_filter = ['badge_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Badge Information', {
            'fields': ('name', 'description', 'badge_type')
        }),
        ('Visual', {
            'fields': ('icon', 'color')
        }),
        ('Requirements', {
            'fields': ('requirement', 'is_active')
        }),
    )


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    readonly_fields = ['earned_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'badge')


# ========== Notification Admin ==========

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('user', 'notification_type', 'title', 'message')
        }),
        ('Link & Status', {
            'fields': ('link', 'is_read')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'Marked {count} notification(s) as read.')
    mark_as_read.short_description = "Mark selected as read"
    
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'Marked {count} notification(s) as unread.')
    mark_as_unread.short_description = "Mark selected as unread"


# ========== User Activity Admin ==========

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['user__username', 'description']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')