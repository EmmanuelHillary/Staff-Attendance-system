from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Office(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
                max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
                max_digits=9, decimal_places=6, null=True, blank=True)
    
class SessionYearModel(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data = ((1, 'Manager'), (2, 'Staff'))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminManager(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile', default='profile/avatar.jpg')
    session_year_id = models.ForeignKey(SessionYearModel, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.admin.username

class Attendance(models.Model):
    attendance_date = models.DateTimeField(auto_now_add=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminManager.objects.create(admin=instance)
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
    
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminmanager.save()
    if instance.user_type == 2:
        instance.staff.save()

