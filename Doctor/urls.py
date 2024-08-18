from django.contrib import admin
from django.urls import path,include

from .views import(
    create_doctor,
    get_all_doctors,
    get_doctor_by_id,
    update_doctor,
    delete_doctor,
    generate_otp,
    verify_otp,
    login,
    forgot_password,
)

urlpatterns = [
    path("create-doctor/",create_doctor),
    path("get_all_doctors/", get_all_doctors),
    path("get_doctor_by_id/",get_doctor_by_id),
    path("update_doctor/", update_doctor),
    path("delete_doctor/", delete_doctor),
    path("generate_otp/",generate_otp),
    path("verify_otp/",verify_otp),
    path("login/",login),
    path("forgot_password/",forgot_password),

]