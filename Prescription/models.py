from django.db import models

# Create your models here.
from django.db import models
import uuid
from Patient.models import Patient
from Appoinment.models import Appointment

class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateTimeField()
    medication = models.TextField()
    dosages = models.TextField()
    online_access = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient.f_name} {self.patient.l_name} on {self.date}"

