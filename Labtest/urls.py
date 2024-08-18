from django.urls import path
from .views import (
    create_labtest, get_all_labtests, get_labtest_by_id,
    update_labtest, delete_labtest
)

urlpatterns = [
    path("create_labtest/", create_labtest),
    path("get_all_labtests/", get_all_labtests),
    path("get_labtest_by_id/<uuid:id>/", get_labtest_by_id),
    path("update_labtest/<uuid:id>/", update_labtest),
    path("delete_labtest/<uuid:id>/", delete_labtest),
]
