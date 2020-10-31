from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.core.mail import send_mail

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        return render(request,'home.html',context={'username':username})
    return render(request,'home.html')

def register(request):
    reg=False
    userform=UserForm()
    profileform=ProfileForm()
    if request.method=="POST" and request.FILES:
        userform=UserForm(request.POST)
        profileform=ProfileForm(request.POST,request.FILES)
        if userform.is_valid() and userform.is_valid():
            user=userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()

            profile=profileform.save(commit=False)
            profile.user=user
            profile.save()
            send_mail('registration','Thanks For registering','harshadvali1432@gmail.com',
            [user.email],fail_silently=False)

            reg=True
            
    return render(request,'register.html',context={'userform':userform,'profileform':profileform,'reg':reg})



def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect((reverse('home')))

        else:
            return HttpResponse('entercorrect details')

    return render(request,'user_login.html')




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def profile_info(request):
    username=request.session.get('username')
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    return render(request,'profile.html',context={'user':user,'profile':profile})
















