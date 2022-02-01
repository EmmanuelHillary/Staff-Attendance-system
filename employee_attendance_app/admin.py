from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Staff, SessionYearModel, Attendance, AttendanceReport

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(SessionYearModel) 
admin.site.register(Attendance) 
admin.site.register(AttendanceReport)
