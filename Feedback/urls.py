from django.urls import path
from .views import (
    create_feedback, get_all_feedbacks, get_feedback_by_id,
    update_feedback, delete_feedback
)

urlpatterns = [
    path("create_feedback/", create_feedback),
    path("get_all_feedbacks/", get_all_feedbacks),
    path("get_feedback_by_id/", get_feedback_by_id),
    path("update_feedback/", update_feedback),
    path("delete_feedback/", delete_feedback),
]
