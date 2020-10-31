from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.core.mail import send_mail

def home(request):
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