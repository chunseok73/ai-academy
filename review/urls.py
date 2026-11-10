from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("", views.lesson_list, name="lesson_list"),
]