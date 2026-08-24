from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from datetime import time
import string

from booking.utils import send_sms  # سرویس پیامک واقعی

User = get_user_model()


# دسته‌بندی سرویس

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("category"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))

    class Meta:
        verbose_name = _("category services")
        verbose_name_plural = _("category's services")

    def __str__(self):
        return self.name


# سرویس / محصول

class Service(models.Model):
    PAYMENT_TYPES = (
        ('full', _('پرداخت کامل')),
        ('down', _('بیعانه')),
    )

    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True, related_name="services", verbose_name=_("دسته‌بندی"))
    name = models.CharField(max_length=150, verbose_name=_("نام سرویس"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    price = models.PositiveIntegerField(default=0, verbose_name=_("قیمت (تومان)"))
    down_payment = models.PositiveIntegerField(default=0, verbose_name=_("بیعانه (تومان)"))
    duration = models.DurationField(verbose_name=_("مدت زمان"))
    payment_type = models.CharField(max_length=4, choices=PAYMENT_TYPES, default='full', verbose_name=_("نوع پرداخت"))
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name=_("تصویر"))
    has_followup = models.BooleanField(default=False, verbose_name=_("نیاز به پیام یادآوری ترمیم دارد؟"))
    followup_days = models.PositiveIntegerField(default=0, verbose_name="روزهای یادآوری" , help_text="مثلا 30،یعنی سی روز بعد از انجام سرویس")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("سرویس")
        verbose_name_plural = _("سرویس‌ها")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_followup_message(self, clint_name):
        return f"سلام{clint_name}وقت ترمیم سرویس شما فرا رسیده{self.name}برای رزرو نوبت جدید با ما تماس بگیرید"


DAYS_OF_WEEK = (
    (0, _('شنبه')),
    (1, _('یکشنبه')),
    (2, _('دوشنبه')),
    (3, _('سه‌شنبه')),
    (4, _('چهارشنبه')),
    (5, _('پنج‌شنبه')),
    (6, _('جمعه')),
)


class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("کارمند"))
    services_offered = models.ManyToManyField(Service, verbose_name=_("خدمات ارائه شده"))
    work_on_saturday = models.BooleanField(default=False, verbose_name=_("شنبه"))
    work_on_sunday = models.BooleanField(default=False, verbose_name=_("یکشنبه"))
    work_on_monday = models.BooleanField(default=False, verbose_name=_("دوشنبه"))
    work_on_tuesday = models.BooleanField(default=False, verbose_name=_("سه‌شنبه"))
    work_on_wednesday = models.BooleanField(default=False, verbose_name=_("چهارشنبه"))
    work_on_thursday = models.BooleanField(default=False, verbose_name=_("پنج‌شنبه"))
    work_on_friday = models.BooleanField(default=False, verbose_name=_("جمعه"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("staff")
        verbose_name_plural = _("staffs")

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class WorkingHours(models.Model):
    staff_member = models.ForeignKey(StaffMember, on_delete=models.CASCADE, verbose_name=_("کارمند"))
    day_of_week = models.PositiveIntegerField(choices=DAYS_OF_WEEK, verbose_name=_("روز هفته"))
    start_time = models.TimeField(verbose_name=_("ساعت شروع"), default=time(9, 0))
    end_time = models.TimeField(verbose_name=_("ساعت پایان"), default=time(23, 0))

    class Meta:
        verbose_name = _("ساعت کاری")
        verbose_name_plural = _("ساعات کاری")
        unique_together = ['staff_member', 'day_of_week']

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_("ساعت شروع باید قبل از ساعت پایان باشد"))

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time}-{self.end_time}"


# پیکربندی سیستم
class Config(models.Model):
    slot_duration = models.PositiveIntegerField(null=True, verbose_name=_("مدت هر نوبت (دقیقه)"))
    lead_time = models.TimeField(null=True, verbose_name=_("زمان شروع کار"))
    finish_time = models.TimeField(null=True, verbose_name=_("زمان پایان کار"))
    appointment_buffer_time = models.PositiveIntegerField(default=0, verbose_name=_("زمان بافر نوبت (دقیقه)"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("تنظیمات")
        verbose_name_plural = _("تنظیمات سیستم")

    def clean(self):
        if Config.objects.exists() and not self.pk:
            raise ValidationError(_("تنها یک پیکربندی می‌تواند وجود داشته باشد"))
        if self.lead_time and self.finish_time and self.lead_time >= self.finish_time:
            raise ValidationError(_("زمان شروع باید قبل از پایان باشد"))

    def save(self, *args, **kwargs):
        self.clean()
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

# نوبت و یادآوری پیامکی


class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("مشتری"))
    staff_member = models.ForeignKey(StaffMember, on_delete=models.SET_NULL, null=True, verbose_name=_("کارمند"))
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, verbose_name=_("سرویس"))
    date = models.DateField(verbose_name=_("تاریخ"))
    start_time = models.TimeField(verbose_name=_("ساعت شروع"))
    end_time = models.TimeField(verbose_name=_("ساعت پایان"))
    total_price = models.PositiveIntegerField(default=0, verbose_name=_("قیمت کل"))
    payment_type = models.CharField(max_length=4, choices=Service.PAYMENT_TYPES, default='full', verbose_name=_("نوع پرداخت"))
    is_paid = models.BooleanField(default=False, verbose_name=_("پرداخت شده"))
    want_reminder = models.BooleanField(default=True, verbose_name=_("ارسال پیام یادآوری"))
    phone_number = models.CharField(
        max_length=15, null=True, blank=True,
        verbose_name=_("شماره تماس مشتری"),
        help_text=_("برای اطلاع‌رسانی پیامکی"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("نوبت")
        verbose_name_plural = _("نوبت‌ها")
        ordering = ['-date', 'start_time']

    def __str__(self):
        return f"{self.client} - {self.service} - {self.date} {self.start_time}"

    # ارسال پیامک با سرویس داخلی
    def send_sms(self, message: str):
        if self.want_reminder and hasattr(self.client, "phone_number") and self.client.phone_number:
            send_sms(self.client.phone_number, message)

    # پیامک رزرو نوبت
    def send_booking_confirmation(self):
        msg = f"نوبت شما برای سرویس {self.service.name} در تاریخ {self.date} ساعت {self.start_time} رزرو شد."
        self.send_sms(msg)

    # پیامک یادآوری قبل از نوبت
    def send_reminder_before_appointment(self, hours_before: int = 3):
        reminder_time = datetime.datetime.combine(self.date, self.start_time) - datetime.timedelta(hours=hours_before)
        if timezone.now() >= reminder_time:
            msg = f"یادآوری: نوبت شما برای سرویس {self.service.name} امروز ساعت {self.start_time} است."
            self.send_sms(msg)

    # پیامک ترمیم خدمات یا تولد
    def send_followup_reminder(self):
        service = self.service
        if not service or not service.has_followup:
            return

        followup_date = self.date + datetime.timedelta(days=service.followup_days)
        if timezone.now().date() >= followup_date:
            msg = f"🌸 سلام {self.client.get_full_name()} عزیز، وقت ترمیم سرویس «{service.name}» شما فرا رسیده است! جهت رزرو مجدد اقدام کنید."
            self.send_sms(msg)
