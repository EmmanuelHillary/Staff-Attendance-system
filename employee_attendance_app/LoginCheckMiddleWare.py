from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class LoginCheckMiddleWare(MiddlewareMixin):
    
    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1": 
                if modulename == "employee_attendance_app.StaffViews":
                    return redirect("manager")
            elif user.user_type == "2":
                if modulename == "employee_attendance_app.StaffViews":
                    pass
                elif modulename == "employee_attendance_app.views" or modulename == "django.views.static":
                    pass
                else:
                    return redirect("staff_home")
            else:
                return redirect('login')

        else:
            if request.path == reverse('login') or request.path == reverse('logout') or modulename == "django.contrib.auth.views" or modulename =="django.contrib.admin.sites":
                pass
            else:
                redirect("login")