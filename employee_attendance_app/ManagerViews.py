from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Staff, SessionYearModel, Attendance, AttendanceReport
from .utils import validate_password, check_user, check_email
from django.core.files.storage import FileSystemStorage
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from datetime import datetime

def admin_home(request):
    total_staffs = Staff.objects.all().count() 
    total_attendances = Attendance.objects.all().count()
    total_present_attendances = AttendanceReport.objects.all().count()
    total_absent_attendances = (total_staffs * total_attendances)  - total_present_attendances
    context = {
        'total_staffs': total_staffs,
        'total_attendances': total_attendances,
        'total_present_attendances': total_present_attendances,
        'total_absent_attendances': total_absent_attendances

    }

    return render(request, 'manager_template/home_content.html', context)

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
            return redirect('add_staff')
        except Exception as e:
            print(e)
            return redirect('add_staff')
    return render(request, 'manager_template/add_staff.html', {'sessions': sessions})

def manage_staff(request):
    staffs = Staff.objects.all().order_by()
    return render(request, 'manager_template/manage_staff.html', {'staffs': staffs})

def edit_staff(request, username):
    sessions = SessionYearModel.objects.all()
    staff = Staff.objects.get(admin__username=username)
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        sex = request.POST.get('sex')
        session = request.POST.get('session')

        profile_pic_url = request.FILES.get('user_profile_picture') or None

        try:
            user = CustomUser.objects.get(username=username)
            user.username = user_username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            
            session_obj = SessionYearModel.objects.get(id=session)
            staff = Staff.objects.get(admin=user)
            staff.address = address
            staff.gender = sex
            staff.session_year_id = session_obj
            if profile_pic_url:
                staff.profile_pic = profile_pic_url
            staff.save()
            messages.success(request, "Successfully Edited Staff")
            return redirect('edit_staff', username=user.username)
        except Exception as e:
            print(e)
            messages.error(request, "Failed to edit staff")
            return redirect('edit_staff', username=username)
    return render(request, 'manager_template/edit_staff.html', {'staff': staff, 'sessions': sessions})

def manage_session(request):
    if request.POST:
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')
        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return redirect('manage_session')
        except:
            messages.error(request, "Failed to Add Session")

    return render(request, 'manager_template/manage_session.html')

def manage_attendance(request):
    sessions = SessionYearModel.objects.all()
    if request.POST:
        attendance = request.POST.get('attendance_date')
        session = request.POST.get('session')
        attendance_status = request.POST.get('attendance_status')
        if attendance_status == "on":
            attendance_status = True
        else:
            attendance_status = False
        try:
            session_obj = SessionYearModel.objects.get(id=session)
            attendance_obj = Attendance(attendance_date=attendance, session_year_id=session_obj, status=attendance_status)
            attendance_obj.save()
            messages.success(request, "Successfully Added Attendance")
            return redirect('manage_attendance')
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Add Attendance")
    return render(request, 'manager_template/manage_attendance.html', {'sessions':sessions})


def attendance_record(request):
    attendances = Attendance.objects.all()
    return render(request, 'manager_template/attendance_record.html', {'attendances':attendances})

def edit_attendance(request, pk):
    sessions = SessionYearModel.objects.all()
    attendance = Attendance.objects.get(id=pk)
    if request.POST:
        session = request.POST.get('session')
        attendance_status = request.POST.get('attendance_status')
        if attendance_status == "on":
            attendance_status = True
        else:
            attendance_status = False
        
        try:
            session_obj = SessionYearModel.objects.get(id=session)
            attendance.session_year_id = session_obj
            attendance.status = attendance_status
            attendance.save()
            messages.success(request, "Successfully Edited Attendance")
            return redirect('edit_attendance', pk=attendance.pk)
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Edit Attendance")

    return render(request, 'manager_template/edit_attendance.html', {'attendance':attendance, 'sessions':sessions})

class AttendanceFilter(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request, *args, **kwargs):
        date = request.data.get('date')
        attendance = Attendance.objects.filter(attendance_date__date=date)
        if attendance.exists():
            attendance = attendance.first() 
        else:
            return Response({'data': []}, status=status.HTTP_200_OK)
        staffs = Staff.objects.all()
        data = []
        for staff in staffs: 
            if AttendanceReport.objects.filter(attendance_id=attendance, staff_id=staff).exists():
                data.append({
                    'staff_first_name': staff.admin.first_name,
                    'staff_last_name': staff.admin.last_name,
                    'attendance': True
                    })
            else:
                data.append({
                'staff_first_name': staff.admin.first_name,
                'staff_last_name': staff.admin.last_name,
                'attendance': False
                })
        return Response({'data': data}, status=status.HTTP_200_OK)

def add_location(request):
    return render(request, 'manager_template/add_location.html')

def manage_location(request):
    return render(request, 'manager_template/manage_location.html')

def edit_location(request, pk):
    return render(request, 'manager_template/edit_location.html')