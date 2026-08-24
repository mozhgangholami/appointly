from django import forms
from .models import Appointment, Service, StaffMember
from django.utils.translation import gettext_lazy as _
from jalali_date.widgets import AdminJalaliDateWidget
from jalali_date.fields import JalaliDateField


class AppointmentForm(forms.ModelForm):
    """فرم رزرو نوبت برای کاربران"""

    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),
        label=_("سرویس"),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    staff_member = forms.ModelChoiceField(
        queryset=StaffMember.objects.select_related('user'),
        label=_("کارمند"),
        widget=forms.Select(attrs={"class": "form-select"})
    )
    # price = forms.ModelChoiceField(
    #     queryset=Service.objects.all(),
    #     label=_("قیمت"),
    #     widget=forms.Select(attrs={"class": "form-select"})
    # )

    date = JalaliDateField(
        label=_("تاریخ"),
        widget=AdminJalaliDateWidget(attrs={'class': 'form-control date-input'})
    )

    TIME_CHOICES = [
        ("06:00", "06:00 قبل‌ظهر"), ("07:00", "07:00 قبل‌ظهر"), ("08:00", "08:00 قبل‌ظهر"),
        ("09:00", "09:00 قبل‌ظهر"), ("10:00", "10:00 قبل‌ظهر"), ("11:00", "11:00 قبل‌ظهر"),
        ("12:00", "12:00 قبل‌ظهر"), ("13:00", "13:00 بعدازظهر"),
        ("14:00", "14:00 بعدازظهر"), ("15:00", "15:00 بعدازظهر"), ("16:00", "16:00 بعدازظهر"),
        ("17:00", "17:00 بعدازظهر"), ("18:00", "18:00 بعدازظهر"), ("19:00", "19:00 بعدازظهر"),
        ("20:00", "20:00 بعدازظهر"), ("21:00", "21:00 بعدازظهر"), ("22:00", "22:00 بعدازظهر"),
        ("23:00", "23:00 بعدازظهر"),
    ]

    start_time = forms.ChoiceField(
        label="ساعت شروع",
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    end_time = forms.ChoiceField(
        label="ساعت پایان",
        choices=TIME_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    phone_number = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "مثلاً 09123456789"})
    )

    class Meta:
        model = Appointment
        fields = ["service", "staff_member", "date", "start_time", "end_time", "want_reminder", "phone_number"]
        widgets = {"date": AdminJalaliDateWidget}
        labels = {
            "want_reminder": _("ارسال پیام یادآوری"),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date < forms.fields.datetime.date.today():
            raise forms.ValidationError(_("تاریخ نمی‌تواند گذشته باشد"))
        return date

    def save(self, commit=True):
        appointment = super().save(commit=False)
        # تعیین قیمت خودکار از سرویس انتخاب‌شده
        appointment.total_price = appointment.service.price
        if commit:
            appointment.save()
        return appointment
