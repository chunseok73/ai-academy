from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("", views.lesson_list, name="lesson_list"),
    path("<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("exercise/<int:exercise_id>/save/", views.save_code, name="save_code"),
]