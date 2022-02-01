from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .EmailBackEnd import EmailBackEnd
from django.contrib import messages
from .models import CustomUser, Staff, SessionYearModel, Attendance, AttendanceReport
from .utils import validate_password, check_user, check_email


def demo_view(request):
    return render(request, 'demo.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackEnd.authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return redirect("manager")
            elif user.user_type == "2":
                return redirect("staff_home")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')

def add_staff(request):
    sessions = SessionYearModel.objects.all()
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')
        sex = request.POST.get('sex')
        session = request.POST.get('session')
        

        profile_pic_url = request.FILES.get('user_profile_picture') or None
        session_obj = SessionYearModel.objects.get(id=session) 

        if not check_user(request, username):
            return redirect('add_staff')
        if not check_email(request, email):
            return redirect('add_staff')
        if not validate_password(request, password):
            return redirect('add_staff')
        try:
            user = CustomUser.objects.create_user(
                username = username,
                email = email,
                first_name = first_name,
                last_name = last_name,
                password = password,
                user_type = 2
            )
            user.staff.address = address
            user.staff.gender = sex
            if profile_pic_url:
                user.staff.profile_pic = profile_pic_url
            user.save()
            staff = Staff.objects.get(admin=user)
            staff.session_year_id = session_obj
            staff.save()
            messages.success(request, "Successfully Added Staff")
            return redirect('login')
        except Exception as e:
            messages.success(request, "Failed to Add Staff")
            return redirect('add_staff')
    return render(request, 'manager_template/add_staff.html', {'sessions': sessions})


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User: "  + request.user.email + " user_type: " + request.user.user_type)  

def logout_user(request):
    logout(request)
    return redirect('login')


