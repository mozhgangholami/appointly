from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from .utils import send_sms


@shared_task
def send_followup_reminders():
    today = timezone.localdate()
    appointments = Appointment.objects.select_related("service", "client")

    for appointment in appointments:
        service = appointment.service
        client = appointment.client

        # فقط برای سرویس‌هایی که ترمیم دارند
        if service.has_followup:
            target_date = appointment.date + timezone.timedelta(days=service.followup_days)
            if target_date == today and client.phone_number:
                msg = f"سلام {client.name} عزیز 🌸 زمان ترمیم {service.name} شما فرا رسیده است!"
                send_sms(client.phone_number, msg)

# @shared_task
# def send_appointment_reminder(appointment_id):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         if appointment.want_reminder and appointment.client.phone_number:
#             msg = f"یادآوری نوبت شما: سرویس {appointment.service.name} در تاریخ {appointment.date} ساعت {appointment.start_time}"
#             send_sms(appointment.client.phone_number, msg)
#     except Appointment.DoesNotExist:
#         pass
#
# @shared_task
# def send_birthday_message(user_id):
#     from django.contrib.auth import get_user_model
#     User = get_user_model()
#     try:
#         user = User.objects.get(id=user_id)
#         if user.phone_number:
#             msg = f"تولدتان مبارک! یک هدیه ویژه برای شما داریم."
#             send_sms(user.phone_number, msg)
#     except User.DoesNotExist:
#         pass
#
# @shared_task
# def send_service_renewal_reminder(appointment_id, days_after=20):
#     try:
#         appointment = Appointment.objects.get(id=appointment_id)
#         target_date = appointment.date + datetime.timedelta(days=days_after)
#         today = timezone.localdate()
#         if today == target_date and appointment.client.phone_number:
#             msg = f"زمان ترمیم {appointment.service.name} شما فرا رسیده است. خوشحال می‌شویم به سالن ما سر بزنید!"
#             send_sms(appointment.client.phone_number, msg)
#     except Appointment.DoesNotExist:
#         pass
