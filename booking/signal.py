# booking/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from .tasks import send_appointment_reminder
from django.utils import timezone
import datetime

@receiver(post_save, sender=Appointment)
def schedule_appointment_reminders(sender, instance, created, **kwargs):
    if created:
        # پیامک تایید فوری
        msg = f"نوبت شما برای سرویس {instance.service.name} در تاریخ {instance.date} ساعت {instance.start_time} رزرو شد."
        from .utils import send_sms
        if instance.client.phone_number:
            send_sms(instance.client.phone_number, msg)

        # پیامک یادآوری ۳ ساعت قبل از شروع
        reminder_time = datetime.datetime.combine(instance.date, instance.start_time) - datetime.timedelta(hours=3)
        from django.utils.timezone import make_aware
        reminder_time_aware = make_aware(reminder_time)
        send_appointment_reminder.apply_async((instance.id,), eta=reminder_time_aware)
