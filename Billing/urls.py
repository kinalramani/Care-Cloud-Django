from django.urls import path
from .views import (
    create_billing, get_all_billings, get_billing_by_id,
    update_billing, delete_billing, get_billings_by_patient,
    get_billings_by_status, get_active_billings, get_deleted_billings
)

urlpatterns = [
    path("create_billing/", create_billing),
    path("get_all_billings/", get_all_billings),
    path("get_billing_by_id/<uuid:id>/", get_billing_by_id),
    path("update_billing/<uuid:id>/", update_billing),
    path("delete_billing/<uuid:id>/", delete_billing),
    path("get_billings_by_patient/<uuid:patient_id>/", get_billings_by_patient),
    path("get_billings_by_status/<str:status>/", get_billings_by_status),
    path("get_active_billings/", get_active_billings),
    path("get_deleted_billings/", get_deleted_billings),
]
