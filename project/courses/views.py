from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course,Lesson,LessonProgress
from django.views.generic import ListView,DetailView
# Create your views here.

class CourseListView(LoginRequiredMixin,ListView):
    model=Course
    template_name='courses/course_list.html'
    context_object_name='courses'

class CourseDetailView(LoginRequiredMixin,DetailView):
    model=Course
    template_name='courses/course_detail.html'
    context_object_name='course'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)

        user=self.request.user
        course=self.object                                                                                                                          #gets the DB object of the self which is 'Course'  #contains the title,description,image from the DB


        context['lessons'] = course.lesson_set.all().order_by('lesson_order')                                                                        #get all the details specified to that particular course
                                                                                                                                                     # how the context looks after adding this
                                                                                                                                                       #{    'course': < Course object: "Django Basics" >,'object': < Courseobject: "Django Basics" >,
                                                                                               #   This is your new key, added by your custom code:          'lesson': < QuerySet [ <Lesson object: "What are Models?" >,< Lesson object: "What are Views?" > ] >}

                                                                                                                                                                                                                                            # this below line is to get the particular data we needed from the DB .if you again ask we are the current user why again use it .Cause the DB has many users and we are one of it .so the particular user is required to get the persoal data not millions of all users data
        completed_ids = LessonProgress.objects.filter(user_link=user,lesson_link__lesson_course=course).values_list('lesson_link_id',flat=True)                                                                                      # listen carefully :if you ever get confusion in this line please dont try to learn this from gemni or google(the last time you did this "you Dumdass wasted 6 hours ,So if you felt like want to understand this line 'please consider sucide as a better idea .kindly from your past ass")
                                                                                                                                                                                                                                            # why did we use 'LessonProgress' cause it allows us to connect to 'User DB(cause we don't want to go and check every user's status,just the current user is enough)'
                                                                                                                                                                                                                                            # In this part '(user_link=user,lesson_link__lesson_course=course)'  don,t overthink just remember 1. we use the LessonProgress to get access to the user DB to get the current user ,which is "  'user_link=user' (note: left side is the DB field name ,right side is the particular or specific data ,we want to access from the DB field on the left side) : here user_link is the field that allows us to connect to the User DB to get data of the current user .But the user alone is not enough .think like we only reduced from checking status of all the user's to the particular user , but now we still have many courses that we would need to check .So we get the current Course using the 'lesson_link__lesson_course=course'.    'now you will be like  why just directly access the course we are using the Course DB currently .Remember you btch that we are searching in the 'LessonProgress DB' not 'Course DB ' in this current line 'why did you do that cause i need the user btch which i could access only be this DB' .So now we have the current user's particular from 100 of other courses we just have to get all the lessons of that course alone which is done by 'value_list('lesson_link_id',flat=True)gives the PK list of all the lessons'  "
        context['completed_lesson_ids'] = set(completed_ids)  # Renamed to be clear


        return context

class LessonDetailView(LoginRequiredMixin,DetailView):
    model=Lesson
    template_name='courses/lesson_detail.html'
    context_object_name='lesson'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)

        lesson=self.object                                #gets the current lesson and its details
        course=lesson.lesson_course                       #gets the course that the lesson belongs to
        current_lesson_order = lesson.lesson_order        #gets the lesson_order of the current lesson (like lesson : 2)
        user=self.request.user                            #gets the login user

        context['next_lsn']=course.lesson_set.filter(lesson_order__gt=current_lesson_order).order_by('lesson_order').first()
        context['prev_lsn']=course.lesson_set.filter(lesson_order__lt=current_lesson_order).order_by('-lesson_order').first()
        context['is_complete']=LessonProgress.objects.filter(user_link=user,lesson_link=lesson).exists()                                    #this line goes to the LessonProgress DBand check if the username and the completed lesson exists




        return context


    def get_queryset(self):                                   #currently not requires
        # For now, let any logged-in user see any lesson.
        # You can add security here later if you want.
        return Lesson.objects.all()


@login_required  # 1. Checks if user is logged in
def mark_lesson_complete(request, pk):                      #this whole thing creates the username and the lesson he completed in the DB
    # 3. Safety check: only run on a button click
    if request.method == 'POST':
        # 4. Get the user and the lesson
        user = request.user
        lesson = get_object_or_404(Lesson, pk=pk)

        # 5. The "magic" command:
        LessonProgress.objects.get_or_create(user_link=user, lesson_link=lesson)

    # 6. The "Go Back" command:
    # This runs *after* the POST or if it's a GET
    return redirect('courses:lesson_detail', pk=pk)
