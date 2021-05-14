from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
import uuid
from django.conf import settings
from django.contrib.auth import logout,authenticate,update_session_auth_hash
from django.contrib.auth import login as user_login
from django.core.mail import message, send_mail
# Create your views here.


# Register Views for User registration
def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1!=password2:
            messages.error(request,"Password doesn't match")
        elif User.objects.filter(username=username).first():
            messages.error(request,"Username is not available")
        elif User.objects.filter(email=email).first():
            messages.error(request,'This email is already registered')
        else:        
            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password1)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_email_after_registration(email,auth_token)
            return render(request,'core/email_sent.html')
    return render(request,'core/register.html')


# Login View for User Login
def login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.error(request,'Username is not registered')
                return redirect('login')
            profile_obj = Profile.objects.filter(user=user_obj).first()
            if not profile_obj.is_verified:
                messages.error(request,'Email is not Verified')
                return redirect('login')
            user = authenticate(username=username,password=password)
            if user is None:
                messages.error(request,'Wrong Password')
                return redirect('login')
            else:
                user_login(request,user)
                return redirect('dashboard')

        return render(request,'core/login.html')
    else:
        return redirect('dashboard')

# Logout View        
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login/')


# Dashboard View
def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request,'core/dashboard.html',{'username':username})
    else:
        return redirect('login')

# Views for email verification

def email_verify(request,auth_token):
    profile_obj = Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.warning(request,'Your account has been already verified')
            return render(request,'core/email_verified.html')
        else:
            profile_obj.is_verified =True
            profile_obj.save()
            messages.success(request,'Your email has been verified, You can Login Now!!')
            return render(request,'core/email_verified.html')
    else:
        messages.error(request,'We are unable to verify your email')
        return render(request,'core/email_verified_error.html')

# Function for sending email
def send_email_after_registration(email,auth_token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://192.168.1.100:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)
