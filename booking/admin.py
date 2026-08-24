from django.contrib import admin
from .models import ServiceCategory, Service, StaffMember, WorkingHours, Config, Appointment
from jalali_date.admin import ModelAdminJalaliMixin


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration", "payment_type", "has_followup", "followup_days")
    list_filter = ("category", "payment_type", "has_followup")
    search_fields = ("name",)
    list_editable = ("has_followup", "followup_days")
    ordering = ("name",)


class WorkingHoursInline(admin.TabularInline):
    model = WorkingHours
    extra = 7
    min_num = 1
    max_num = 7


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("user",)
    inlines = [WorkingHoursInline]


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("slot_duration", "lead_time", "finish_time", "appointment_buffer_time")


@admin.register(Appointment)
class AppointmentAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ("client", "staff_member", "service", "date", "start_time", "is_paid", "want_reminder")
    list_filter = ("date", "is_paid", "want_reminder")
    search_fields = ("client__username", "service__name")
    ordering = ("-date", "start_time")

    # برای ارسال سریع پیامک از پنل ادمین
    actions = ["send_reminder_now"]

    def send_reminder_now(self, request, queryset):
        """ارسال پیام یادآوری به صورت دستی از پنل ادمین"""
        count = 0
        for appointment in queryset:
            appointment.send_reminder_message()
            count += 1
        self.message_user(request, f"✅ پیام یادآوری برای {count} نوبت ارسال شد.")
    send_reminder_now.short_description = "📨 ارسال پیام یادآوری"

