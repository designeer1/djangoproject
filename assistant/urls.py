from django.urls import path
from .views import process_command  # Correct import


urlpatterns = [
    path("process_command/", process_command, name="process_command"),
]
