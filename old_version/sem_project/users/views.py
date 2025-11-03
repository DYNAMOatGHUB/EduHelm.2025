from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegisterForm,UpdateUserForm,ProfileUpdateForm

def register(request):
    if request.method == "POST":                                                                            #This checks if the request is GET or POST (GET means "someone has just entered the register") and (POST means "someone has entered the register page and typed the details and since in the register.htlm we used POST .it returns back to the views.py file as POST along with the user typed data")                                                                                                  #request.method = it is like either request.POST or request.GET
        form=UserRegisterForm(request.POST)                                #request.POST is used to immediatly get the form data that we just submitted                                      #Here is the actual validation procces occurs like username ,password validation
        if form.is_valid():
            user=form.save()                                                                                     #If the form is valid data then here the form is saved in DB
            username=form.cleaned_data.get('username')                                                      #Here we get the username for the flash message and cleaned_data  gives the data in a python radable formate
            messages.success(request,f'Account created for {username}')
            login(request, user)#messages.success stores the message temporarily and it is passed to the templates automatically .The actuall message printing work is done in the base.html
            return redirect('sample_home')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


@login_required(login_url='login')
def profile(request):
    context = {}
    return render(request, 'users/profile.html',context)

def logout_confirm(request):
    return render(request, 'users/logout_confirm.html')

def profile_edit(request):
    if request.method == "POST":
        u_form = UpdateUserForm(request.POST,instance=request.user)  # instance=parameter is used to update the existing data
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={'u_form':u_form,'p_form':p_form}
    return render(request, 'users/profile_edit.html',context)