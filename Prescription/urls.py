from django.urls import path
from .views import (
    create_prescription, get_prescription, get_prescription_by_id,
    update_prescription, delete_prescription, get_prescriptions_by_patient
)

urlpatterns = [
    path("create_prescription/", create_prescription),
    path("get_prescription/", get_prescription),
    path("get_prescription_by_id/", get_prescription_by_id),
    path("update_prescription/", update_prescription),
    path("delete_prescription/", delete_prescription),
    path("get_prescriptions_by_patient/", get_prescriptions_by_patient),
]
