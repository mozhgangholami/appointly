from django.test import TestCase
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import admin
from accounts.admin import CustomUserAdmin
from django.urls import reverse
from django.test import Client

User = get_user_model()


class CustomUserCreationFormTest(TestCase):
    def test_valid_form_creates_user(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "mas12345",
            "password2": "mas12345",
        }
        form = CustomUserCreationForm(form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("mas12345"))

    def test_form_invalid_without_email(self):
        form_data = {"username": "testuser",
                     "email": "test@exampel.com",
                     "password1": "mas12345",
                     "password2": "wxy12345",
                     }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class CustomUserModelTest(TestCase):
    def test_create_user_with_extera_fields(self):
        user = User.objects.create_user(
            username="mozhgangh",
            email="mozhgangh@gh.com",
            password="900800",
            age="32",
            phone_number="09100000000",
            gender="F"
        )
        self.assertEqual(user.username, "mozhgangh")
        self.assertEqual(user.email, "mozhgangh@gh.com")
        self.assertEqual(user.check_password, "900800")
        self.assertEqual(user.age, 32)
        self.assertEqual(user.phone_number, "0910000000")
        self.assertEqual(user.gender, "F")

    def test_str_method_returns_full_name_is_present(self):
        user = User.objects.create_user(
            username="mozhgangh",
            password="900800",
            first_name="mozhgan",
            last_name="gh"
        )
        self.assertEqual(str(user), "mozhgangh")

    def test_phone_number_can_be_blank(self):
        user = User.objects.create_user(
            username="no_phone",
            password="Test12345",
            phone_number="",
        )
        self.assertEqual(user.phone_number, "")

    def test_gender_choices(self):
        user = User.objects.create_user(
            username="mozhgangh",
            password="900800",
            gender="M",
        )
        self.assertEqual(user.gender, "M")


class CustomUserAdminTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="mozhgangh",
            email="mozhgangh@gh.com",
            password="900800",
        )
        self.client = Client()
        self.client.force_login(self.admin_user)

    def test_custom_user_registered_in_admin(self):
        self.assertIn(User, admin.site._registry)
        self.assertIsInstance(admin.site._registry[User], CustomUserAdmin)

    def test_list_display_fields(self):
        self.assertEqual(
            CustomUserAdmin.list_display, ("email", "username", "is_staff", "is_active", "age", "phone_number")
        )

    def test_search_fields(self):
        self.assertEqual(CustomUserAdmin.search_fields, ("email", "username"))

    def test_ordering(self):
        self.assertEqual(CustomUserAdmin.ordering, ("email", ))

    def test_admin_changelist_page_load(self):
        url = reverse("admin:accounts_customuser_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_add_page_loads(self):
        url = reverse("admin:accounts_customuser_add")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
