# 🎓 EduHelm - Educational Platform

A comprehensive educational platform built with Django and MongoDB, featuring study tracking, course management, collaborative learning, and AI-powered mentorship.

## 🌟 Features

### ✅ Phase 1-4: Core Features
- **User Authentication & Profiles**: Secure login, registration, profile management
- **Study Tracking**: Track study sessions, set goals, view analytics
- **Notes & Resources**: Create, organize, and share study materials
- **Category Management**: Organize content by topics
- **Course Management**: Browse courses, enroll, track progress

### ✅ Phase 5: Collaborative Learning
- **Study Groups**: Create and join study groups
- **Discussions**: Topic-based discussions with replies
- **Peer Reviews**: Review and rate peer submissions
- **Real-time Notifications**: Stay updated with group activities
- **Leaderboards & Badges**: Gamification for motivation

## 🛠️ Technology Stack

- **Backend**: Django 3.1.12
- **Database**: MongoDB (via Djongo ORM)
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome
- **Python**: 3.11.9

## 📋 Prerequisites

- Python 3.11.9
- MongoDB 8.0
- Git

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/eduhelm.git
cd eduhelm
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
cd project
pip install -r requirements.txt
```

### 4. Configure MongoDB
- Make sure MongoDB is running on `localhost:27017`
- Database name: `eduhelm_db`

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Local**: http://127.0.0.1:8000
- **Custom Domain** (after setup): http://eduhelm.local:8000

## 🌐 Custom Domain Setup (Optional)

Run as Administrator:
```bash
SETUP_CUSTOM_DOMAIN.bat
```

Then access at: `http://eduhelm.local:8000`

## 📁 Project Structure

```
sem_project/
├── project/
│   ├── project_1/          # Main settings
│   ├── users/              # User management, profiles, study tracking
│   ├── courses/            # Course management
│   ├── sample/             # Dashboard
│   ├── media/              # User uploads
│   └── manage.py
├── .venv/                  # Virtual environment (not in git)
├── requirements.txt
└── README.md
```

## 📚 Documentation

- [Site Fixed Guide](SITE_FIXED_GUIDE.md) - Troubleshooting
- [Custom Domain Setup](CUSTOM_DOMAIN_SETUP.md) - Local domain configuration
- [Phase 5 Implementation](PHASE_5_IMPLEMENTATION_COMPLETE.md) - Collaborative features

## 🔧 Key Configuration

### Database (settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'eduhelm_db',
        'CLIENT': {
            'host': 'localhost',
            'port': 27017,
        }
    }
}
```

### Allowed Hosts
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'eduhelm.local', 'www.eduhelm.local']
```

## 🎯 Available Features

### Study Tracking
- Start/End study sessions
- Set study goals with deadlines
- View analytics and statistics
- Track study streak

### Courses
- Browse course catalog
- Enroll in courses
- Track lesson progress
- Complete lessons

### Collaborative Learning
- Create/Join study groups
- Participate in discussions
- Submit peer reviews
- Earn badges

### Resources
- Upload study materials
- Share resources publicly
- Organize by categories
- Search and filter

## 🐛 Troubleshooting

### MongoDB Connection Issues
Ensure MongoDB is running:
```bash
mongod --dbpath "C:\data\db"
```

### Profile Errors
Run profile cleanup:
```bash
python force_clean_profiles.py
```

### Server Won't Start
Check if port 8000 is available or use different port:
```bash
python manage.py runserver 8080
```

## 👥 Contributors

- Developer: Your Name
- Institution: SIET AIDS 2024-28

## 📄 License

This project is for educational purposes.

## 🚀 Future Enhancements

- [ ] AI Mentor System
- [ ] Mobile App
- [ ] Video Lessons
- [ ] Live Study Sessions
- [ ] Integration with Learning Management Systems

---

**Built with ❤️ for better learning**

*Last Updated: November 1, 2025*
