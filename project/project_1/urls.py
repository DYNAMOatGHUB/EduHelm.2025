"""
URL configuration for project_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sample.urls')),
    path('courses/', include('courses.urls')),
    path('', include('users.urls')),  # Study tracking URLs
    path('register/', user_views.register, name='register'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('profile/',user_views.profile,name='profile'),
    path('logout/confirm',user_views.logout_confirm,name='logout_confirm'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)                                       #this tells the django that we are on the development server and allow us to use sent and receive .Normally we ccant do that cause django isnt meant for media purpose .so it normally blocks request that comes with /media/

