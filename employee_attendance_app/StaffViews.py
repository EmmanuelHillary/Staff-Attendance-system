from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Staff, AttendanceReport, Attendance, SessionYearModel
from datetime import datetime

def staff_home(request):
    staff = Staff.objects.get(admin__username=request.user.username)
    total_attendance = Attendance.objects.all().count()
    present_attendance = AttendanceReport.objects.filter(staff_id=staff).count()
    absent_attendance = total_attendance - present_attendance
    attendance = Attendance.objects.filter(status=True).order_by('-updated_at').first()
    check_attendance = AttendanceReport.objects.filter(staff_id=staff, attendance_id=attendance).exists()
    return render(request, 'staff_template/home_content.html', {'total_attendance': total_attendance, 'present_attendance': present_attendance, 'absent_attendance': absent_attendance, 'date': attendance.attendance_date, 'check_attendance': check_attendance})

def edit_profile(request):
    sessions = SessionYearModel.objects.all()
    staff = Staff.objects.get(admin__username=request.user.username)
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
            user = CustomUser.objects.get(username=request.user.username)
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
            return redirect('edit_profile')
        except Exception as e:
            print(e)
            messages.error(request, "Failed to edit staff")
            return redirect('edit_profile')
    return render(request, 'staff_template/edit_profile.html', {'staff': staff, 'sessions': sessions})

def take_attendance(request):
    attendance_reports = Attendance.objects.all()
    staff = Staff.objects.get(admin__username=request.user.username)
    staff_attendances = AttendanceReport.objects.filter(staff_id=staff)
    return render(request, 'staff_template/take_attendance.html', {'attendances': attendance_reports, 'staff_attendances':staff_attendances})

def mark_attendance(request):
    attendance_reports = AttendanceReport.objects.all()
    staff = Staff.objects.get(admin__username=request.user.username)
    attendance = Attendance.objects.filter(status=True).order_by('-updated_at').first()
    if AttendanceReport.objects.filter(staff_id=staff, attendance_id=attendance).exists():
        pass
    elif attendance.attendance_date.date() != datetime.now().date():
        messages.error(request, "Failed to Mark Attendance")
        return redirect('staff_home')
    else:
        try:
            attendance_reports = AttendanceReport.objects.create(
                staff_id = staff,
                attendance_id = attendance,
                status=True
            )
            attendance_reports.save()
            messages.success(request, "Successfully Marked Attendance")
            return redirect('staff_home')
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Mark Attendance")
            return redirect('staff_home')
    return redirect('staff_home')