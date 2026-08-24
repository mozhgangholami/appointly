from datetime import timedelta
from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AppointmentForm
from .models import Appointment, Config, WorkingHours
from .utils import send_sms
from .utils import send_sms_notification


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "booking/book_appointment.html"
    success_url = reverse_lazy("booking:appointment_list")

    def form_valid(self, form):
        print("🔹 شروع form_valid")

        appointment = form.save(commit=False)

        # 🧩 بررسی اطلاعات حیاتی (تا None وارد کوئری نشه)
        if not appointment.staff_member:
            form.add_error("staff_member", "کارمند انتخاب نشده است.")
            return self.form_invalid(form)

        if not appointment.date:
            form.add_error("date", "تاریخ انتخاب نشده است.")
            return self.form_invalid(form)

        if not appointment.start_time:
            form.add_error("start_time", "ساعت شروع انتخاب نشده است.")
            return self.form_invalid(form)

        if not appointment.service:
            form.add_error("service", "سرویس انتخاب نشده است.")
            return self.form_invalid(form)

        # ✅ محاسبه ساعت پایان نوبت
        from django.utils import timezone
        try:
            proposed_end_dt = timezone.datetime.combine(
                appointment.date, appointment.start_time
            ) + appointment.service.duration
            appointment.end_time = proposed_end_dt.time()
        except Exception as e:
            print(f"❌ خطا در محاسبه زمان پایان: {e}")
            form.add_error("start_time", "مدت زمان سرویس مشخص نیست.")
            return self.form_invalid(form)

        # ✅ ذخیره در دیتابیس
        appointment.client = self.request.user
        appointment.phone_number = form.cleaned_data.get("phone_number")
        appointment.save()

        print(f"✅ نوبت ثبت شد: {appointment.service.name} - {appointment.date} {appointment.start_time}")
        print(f"📞 شماره تماس ثبت شده در فرم: {appointment.phone_number}")

        # ✅ پیام موفقیت در سایت
        from django.contrib import messages
        messages.success(
            self.request,
            f"نوبت شما برای سرویس «{appointment.service.name}» با موفقیت ثبت شد."
        )

        # ✅ ارسال پیامک (در صورت وجود شماره)
        if appointment.phone_number:
            print(f"🛰 در حال ارسال پیام به شماره {appointment.phone_number} ...")
            from .utils import send_sms_notification
            send_sms_notification(
                phone_number=appointment.phone_number,
                message=f"✅ نوبت شما برای سرویس «{appointment.service.name}» در تاریخ {appointment.date} ساعت {appointment.start_time} با موفقیت ثبت شد."
            )
        else:
            print("⚠️ شماره تماس در فرم وجود ندارد. پیامک ارسال نشد.")

        print("🔹 پایان form_valid")
        return super().form_valid(form)


class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = "booking/appointment_list.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.filter(client=self.request.user).order_by("-date", "start_time")


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = "booking/appointment_detail.html"
    context_object_name = "appointment"

    def get_queryset(self):
        # فقط نوبت‌های کاربر جاری
        return Appointment.objects.filter(client=self.request.user)

