from django.urls import path
from . import views

urlpatterns = [
    # Profile management
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Study tracking URLs
    path('study/', views.study_dashboard, name='study_dashboard'),
    path('study/start/', views.start_session, name='start_session'),
    path('study/end/', views.end_session, name='end_session'),
    path('study/history/', views.study_history, name='study_history'),
    path('study/analytics/', views.study_analytics, name='study_analytics'),
    path('study/goals/', views.manage_goals, name='manage_goals'),
    path('study/goals/delete/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    
    # Notes URLs
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:note_id>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:note_id>/pin/', views.toggle_note_pin, name='toggle_note_pin'),
    path('notes/<int:note_id>/favorite/', views.toggle_note_favorite, name='toggle_note_favorite'),
    
    # Categories URLs
    path('notes/categories/', views.categories_manage, name='categories_manage'),
    path('notes/categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    
    # Resources URLs
    path('resources/', views.resources_library, name='resources_library'),
    path('resources/upload/', views.resource_upload, name='resource_upload'),
    path('resources/<int:resource_id>/', views.resource_view, name='resource_view'),
    path('resources/<int:resource_id>/delete/', views.resource_delete, name='resource_delete'),
    
    # Study Groups URLs
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/join/', views.group_join, name='group_join'),
    path('groups/<int:group_id>/leave/', views.group_leave, name='group_leave'),
    path('groups/<int:group_id>/delete/', views.group_delete, name='group_delete'),
    
    # Discussion URLs
    path('groups/<int:group_id>/discussions/', views.discussion_list, name='discussion_list'),
    path('groups/<int:group_id>/discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/<int:discussion_id>/delete/', views.discussion_delete, name='discussion_delete'),
    
    # Peer Review URLs
    path('review/<str:target_type>/<int:target_id>/', views.add_review, name='add_review'),
    
    # Notification URLs (AJAX endpoints)
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('api/notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    
    # Badge URLs
    path('api/badges/', views.get_user_badges, name='get_user_badges'),
    path('api/badges/check/', views.check_badge_eligibility, name='check_badge_eligibility'),
    
    # Activity Feed URL
    path('api/activity/', views.get_activity_feed, name='get_activity_feed'),
]

