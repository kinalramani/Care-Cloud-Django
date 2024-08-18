from django.contrib import admin
from django.urls import path
from .views import verify_otp

from .views import(
    create_patient,
    get_all_patients,
    get_patient_by_id,
    update_patient,
    delete_patient,
    generate_otp,
    verify_otp,
    login,
    forgot_password,
    decode_token_view
)

urlpatterns = [
    path("create_patient/",create_patient),
    path("get_all_patients/", get_all_patients),
    path("get_patient_by_id/",get_patient_by_id),
    path("update_patient/", update_patient),
    path("delete_patient/", delete_patient),
    path("generate_otp/",generate_otp),
    path("verify_otp/",verify_otp),
    path("login/",login),
    path("forgot_password/",forgot_password),
    path("decode_token/",decode_token_view),
]