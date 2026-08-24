# from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", "first_name", "last_name", "email",
            "phone_number", "password1", "password2",
            "gender", "age"
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", "first_name", "last_name", "email",
            "phone_number", "gender", "age",
            "is_active", "is_staff"
        )


# class CustomSignupForm(SignupForm):
#     phone_number = forms.CharField(
#         max_length=11,
#         label="شماره موبایل",
#         required=True,
#         widget=forms.TextInput(attrs={'placeholder': 'مثلاً 09123456789'})
#     )
#
#     age = forms.IntegerField(label="سن", required=False)
#
#     gender = forms.ChoiceField(
#         label="جنسیت",
#         choices=[('M', 'مرد'), ('F', 'زن')],
#         required=False
#     )
#
#     def save(self, request):
#         # ذخیره فرم اصلی allauth
#         user = super().save(request)
#         # ذخیره فیلدهای اضافی
#         user.phone_number = self.cleaned_data['phone_number']
#         user.age = self.cleaned_data.get('age')
#         user.gender = self.cleaned_data.get('gender')
#         user.save()
#         return user
