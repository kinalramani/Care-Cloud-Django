from django.urls import path
from .views import (
    create_appointment, get_all_appointments, get_appointment_by_id,
    update_appointment, delete_appointment
)

urlpatterns = [
    path("create_appointment/", create_appointment),
    path("get_all_appointments/", get_all_appointments),
    path("get_appointment_by_id/", get_appointment_by_id),
    path("update_appointment/", update_appointment),
    path("delete_appointment/", delete_appointment),
]