from django.contrib import messages
from django.shortcuts import redirect
from .models import CustomUser
import re

def validate_password(request, password):
    if len(password) < 8:
        messages.error(request, "password must be at least 8 characters.")
        return False
    if not re.findall('\d', password):
        messages.error(request, "The password must contain at least 1 digit.")
        return False
    if not re.findall('[A-Z]', password):
        messages.error(request, "The password must contain at least 1 uppercase letter.")
        return False
    if not re.findall('[a-z]', password):
        messages.error(request, "The password must contain at least 1 lowercase letter.")
        return False
    return True

def check_user(request, username): 
    if CustomUser.objects.filter(username=username).exists():
        messages.error(request, "Username already exists.")
        return False
    return True

def check_email(request, email): 
    if CustomUser.objects.filter(email=email).exists():
        messages.error(request, "Email already exists.")
        return False
    return True