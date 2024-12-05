from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/edit_review/<int:review_id>', views.edit_review, name="edit_review"),
    path('<int:product_id>/delete_review/<int:review_id>', views.delete_review, name="delete_review")
]