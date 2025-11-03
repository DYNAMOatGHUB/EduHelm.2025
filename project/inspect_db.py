"""
Quick database inspection script
Usage: python inspect_db.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_1.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import Profile, StudySession, Goal, Note, Category
from courses.models import Course, Lesson, Enrollment

def inspect_database():
    print("=" * 60)
    print("DATABASE INSPECTION")
    print("=" * 60)
    
    # Users
    print(f"\n👤 USERS: {User.objects.count()}")
    for user in User.objects.all()[:5]:
        print(f"   - {user.username} ({user.email}) - {'Staff' if user.is_staff else 'User'}")
    
    # Profiles
    print(f"\n📝 PROFILES: {Profile.objects.count()}")
    for profile in Profile.objects.all()[:5]:
        print(f"   - {profile.user.username} - Mentor: {profile.is_mentor}")
    
    # Courses
    print(f"\n📚 COURSES: {Course.objects.count()}")
    for course in Course.objects.all()[:5]:
        print(f"   - {course.title} by {course.instructor.username}")
    
    # Lessons
    print(f"\n📖 LESSONS: {Lesson.objects.count()}")
    
    # Enrollments
    print(f"\n🎓 ENROLLMENTS: {Enrollment.objects.count()}")
    
    # Study Sessions
    print(f"\n⏱️  STUDY SESSIONS: {StudySession.objects.count()}")
    
    # Goals
    print(f"\n🎯 GOALS: {Goal.objects.count()}")
    
    # Notes
    print(f"\n📝 NOTES: {Note.objects.count()}")
    
    # Categories
    print(f"\n🔖 CATEGORIES: {Category.objects.count()}")
    
    print("\n" + "=" * 60)
    print("Database location: db.sqlite3")
    print("=" * 60)

if __name__ == '__main__':
    inspect_database()
