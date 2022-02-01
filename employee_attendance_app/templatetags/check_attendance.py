from django import template
from employee_attendance_app.models import AttendanceReport, Attendance, Staff

register = template.Library()

@register.simple_tag
def check_status(attendance, user):
    attendance_date = Attendance.objects.get(attendance_date=attendance)
    staff = Staff.objects.get(admin__username=user)
    if AttendanceReport.objects.filter(attendance_id=attendance_date, staff_id=staff).exists():
        return True
    return False

register.filter('check_status', check_status)
