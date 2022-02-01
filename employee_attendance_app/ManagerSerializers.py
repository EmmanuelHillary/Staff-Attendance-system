from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    model = Staff
    fields = "__all__"
