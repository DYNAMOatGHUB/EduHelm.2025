# 🎓 EduHelm - Online Learning Platform# 🎓 EduHelm - Educational Platform



A comprehensive Django-based learning management system featuring courses, mentorship, study tracking, and collaborative learning.A comprehensive educational platform built with Django and MongoDB, featuring study tracking, course management, collaborative learning, and AI-powered mentorship.



## 🌟 Live Demo## 🌟 Features



**Production Site:** https://eduhelm-2025.onrender.com### ✅ Phase 1-4: Core Features

- **User Authentication & Profiles**: Secure login, registration, profile management

**Login Credentials:**- **Study Tracking**: Track study sessions, set goals, view analytics

- Username: `admin`- **Notes & Resources**: Create, organize, and share study materials

- Password: `Admin@2025`- **Category Management**: Organize content by topics

- **Course Management**: Browse courses, enroll, track progress

## ✨ Features

### ✅ Phase 5: Collaborative Learning

### Core Features- **Study Groups**: Create and join study groups

- 📚 **Course Management** - Create, browse, and enroll in courses- **Discussions**: Topic-based discussions with replies

- 👨‍🏫 **Mentor System** - Connect with mentors for guidance- **Peer Reviews**: Review and rate peer submissions

- 📖 **Lesson Viewing** - Structured learning with lessons- **Real-time Notifications**: Stay updated with group activities

- 👤 **User Profiles** - Personalized profiles with bios and roles- **Leaderboards & Badges**: Gamification for motivation

- 🔐 **Authentication** - Secure login/registration system

## 🛠️ Technology Stack

### Study & Progress Tracking

- ⏱️ **Study Sessions** - Track your learning time- **Backend**: Django 3.1.12

- 📊 **Progress Tracking** - Monitor your journey- **Database**: MongoDB (via Djongo ORM)

- 🎯 **Goals & Milestones** - Set and achieve learning goals- **Frontend**: HTML5, CSS3, JavaScript

- 📈 **Statistics Dashboard** - View learning analytics- **Icons**: Font Awesome

- **Python**: 3.11.9

### Collaborative Learning

- 💬 **Discussion Forums** - Topic-based discussions## 📋 Prerequisites

- 👥 **Study Groups** - Collaborative learning spaces

- ⭐ **Course Reviews** - Rate and review courses- Python 3.11.9

- 🏆 **Leaderboards** - Gamification elements- MongoDB 8.0

- Git

### Resources

- 📝 **Notes Management** - Create and organize notes## 🚀 Quick Start

- 📂 **File Sharing** - Share study materials

- 🔖 **Categories** - Organize content by topics### 1. Clone Repository

```bash

## 🛠️ Tech Stackgit clone https://github.com/YOUR_USERNAME/eduhelm.git

cd eduhelm

- **Framework:** Django 3.1.12```

- **Database:** SQLite

- **Static Files:** WhiteNoise### 2. Create Virtual Environment

- **Styling:** Custom CSS + Font Awesome```bash

- **Deployment:** Renderpython -m venv .venv

- **Python:** 3.11.9.venv\Scripts\activate  # Windows

```

## 🚀 Quick Start

### 3. Install Dependencies

### Local Development```bash

cd project

1. **Clone the repository**pip install -r requirements.txt

```bash```

git clone https://github.com/DYNAMOatGHUB/EduHelm.2025.git

cd EduHelm.2025/project### 4. Configure MongoDB

```- Make sure MongoDB is running on `localhost:27017`

- Database name: `eduhelm_db`

2. **Create virtual environment**

```bash### 5. Run Migrations

python -m venv .venv```bash

.venv\Scripts\activate  # Windowspython manage.py migrate

source .venv/bin/activate  # Linux/Mac```

```

### 6. Create Superuser

3. **Install dependencies**```bash

```bashpython manage.py createsuperuser

pip install -r requirements.txt```

```

### 7. Start Server

4. **Run migrations**```bash

```bashpython manage.py runserver

python manage.py migrate```

```

### 8. Access Application

5. **Create admin user**- **Local**: http://127.0.0.1:8000

```bash- **Custom Domain** (after setup): http://eduhelm.local:8000

python manage.py createadmin

```## 🌐 Custom Domain Setup (Optional)



6. **Run development server**Run as Administrator:

```bash```bash

python manage.py runserverSETUP_CUSTOM_DOMAIN.bat

``````



7. **Visit:** http://127.0.0.1:8000Then access at: `http://eduhelm.local:8000`



## 📁 Project Structure## 📁 Project Structure



``````

project/sem_project/

├── courses/          # Course management├── project/

├── sample/           # Landing pages│   ├── project_1/          # Main settings

├── users/            # Authentication & profiles│   ├── users/              # User management, profiles, study tracking

├── project_1/        # Settings│   ├── courses/            # Course management

├── media/            # User uploads│   ├── sample/             # Dashboard

├── staticfiles/      # Static files│   ├── media/              # User uploads

└── manage.py│   └── manage.py

```├── .venv/                  # Virtual environment (not in git)

├── requirements.txt

## 🌐 Live Deployment└── README.md

```

**URL:** https://eduhelm-2025.onrender.com

## 📚 Documentation

See `RENDER_POST_DEPLOY.md` for deployment details.

- [Site Fixed Guide](SITE_FIXED_GUIDE.md) - Troubleshooting

## 📄 License- [Custom Domain Setup](CUSTOM_DOMAIN_SETUP.md) - Local domain configuration

- [Phase 5 Implementation](PHASE_5_IMPLEMENTATION_COMPLETE.md) - Collaborative features

MIT License - Open source

## 🔧 Key Configuration

## 👥 Team

### Database (settings.py)

**Developer:** DYNAMOatGHUB | **Institution:** SIET AIDS 2024-28```python

DATABASES = {

---    'default': {

        'ENGINE': 'djongo',

**Made with ❤️ for better learning** • *Updated: November 3, 2025*        'NAME': 'eduhelm_db',

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
