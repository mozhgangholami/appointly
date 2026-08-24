from django.urls import path
from .views import AppointmentCreateView, AppointmentListView, AppointmentDetailView

app_name = "booking"

urlpatterns = [
    path("book/", AppointmentCreateView.as_view(), name="book_appointment"),
    path("my-appointments/", AppointmentListView.as_view(), name="appointment_list"),
    path("appointment/<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
]
