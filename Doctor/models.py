

# Create your models here.
from django.db import models
import uuid


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Store the hashed password
    gender = models.CharField(max_length=10)
    specialization = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    address = models.TextField()
    available_slots = models.TextField()  # Assuming this is a JSON or similar representation of available slots
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_verify = models.BooleanField(default=False)



    def __str__(self):
        return f"Dr. {self.f_name} {self.l_name}"
    


from django.utils import timezone


class Otp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    email = models.EmailField(max_length=32, null=False)
    otp = models.CharField(max_length=6, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"OTP for {self.otp}"