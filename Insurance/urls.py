from django.urls import path
from .views import (
    create_insurance, get_all_insurances, get_insurance_by_id,
    update_insurance, delete_insurance,get_insurances_by_patient,restore_insurance
)

urlpatterns = [
    path("create_insurance/", create_insurance),
    path("get_all_insurances/", get_all_insurances),
    path("get_insurance_by_id/", get_insurance_by_id),
    path("update_insurance/<uuid:id>/", update_insurance),
    path("delete_insurance/<uuid:id>/", delete_insurance),
    path("get_insurances_by_patient/", get_insurances_by_patient),
    path("restore_insurance/", restore_insurance),

]
