from django.urls import path

from .views import demo_view, login_user, logout_user, GetUserDetails, add_staff
from .ManagerViews import admin_home, manage_staff, edit_staff, manage_session, manage_attendance, attendance_record, edit_attendance, AttendanceFilter, manage_location, add_location, edit_location
from .StaffViews import staff_home, take_attendance, mark_attendance, edit_profile

urlpatterns = [
    path('demo/', demo_view),
    path('', login_user, name='login'),
    path('user/', GetUserDetails, name="user_detail"),
    path('logout/', logout_user, name="logout"),
    path('manager/', admin_home, name="manager"),
    path('add-staff/', add_staff, name="add_staff"),
    path('manage-staff/', manage_staff, name="manage_staff"),
    path('edit-profile/', edit_profile, name="edit_profile"),
    path('edit-staff/<str:username>', edit_staff, name="edit_staff"),
    path('staff-home/', staff_home, name="staff_home"),
    path('manage-session/', manage_session, name="manage_session"),
    path('manage-attendance/', manage_attendance, name="manage_attendance"),
    path('attendance-record/', attendance_record, name="attendance_record"),
    path('edit-attendance/<int:pk>/', edit_attendance, name="edit_attendance"),
    path('check-attendance/', take_attendance, name="take_attendance"),
    path('mark-attendance/', mark_attendance, name="mark_attendance"),
    path('add-location/', add_location, name="add_location"),
    path('manage-location/', manage_location, name="manage_location"),
    path('edit-location/<int:pk>/', edit_location, name="edit_location"),
    path('attendance-filter/', AttendanceFilter.as_view(), name="attendance_filter"),
]