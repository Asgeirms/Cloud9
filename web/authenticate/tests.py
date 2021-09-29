from django.test import TestCase
from django.urls import reverse
from .forms import UserRegisterForm
from .models import User

class UserRegisterFormTests(TestCase):

    def setUp(self):
        self.valid_form_data = {
            "username": "NewTestUser",
            "first_name": "test", "last_name":
            "user", "email": "testing@test.no",
            "password1": "passwordtest1234",
            "password2": "passwordtest1234"
        }

    def test_create_user_success(self):
        self.assertFalse(User.objects.exists())
        response = self.client.post(url, data=self.valid_form_data)
        self.assertTrue(User.objects.filter(username = "NewTestUser").exists())

    def test_valid_user_register_form(self):
        valid_form = UserRegisterForm(data=self.valid_form_data)
        self.assertTrue(valid_form.is_valid())

    def test_user_register_form_missing_username(self):
        missing_username_data = self.valid_form_data
        missing_username_data['username'] = None
        invalid_form = UserRegisterForm(data=missing_username_data)
        self.assertFalse(invalid_form.is_valid())
    
    def test_user_register_form_missing_first_name(self):
        missing_first_name_data = self.valid_form_data
        missing_first_name_data['first_name'] = None
        invalid_form = UserRegisterForm(data=missing_first_name_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_missing_last_name(self):
        missing_last_name_data = self.valid_form_data
        missing_last_name_data['last_name'] = None
        invalid_form = UserRegisterForm(data=missing_last_name_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_missing_email(self):
        missing_email_data = self.valid_form_data
        missing_email_data['email'] = None
        invalid_form = UserRegisterForm(data=missing_email_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_missing_password1(self):
        missing_password1_data = self.valid_form_data
        missing_password1_data['password1'] = None
        invalid_form = UserRegisterForm(data=missing_password1_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_missing_password2(self):
        missing_password2_data = self.valid_form_data
        missing_password2_data['password1'] = None
        invalid_form = UserRegisterForm(data=missing_password2_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_password_not_matching(self):
        not_matching_passwords_data = self.valid_form_data
        not_matching_passwords_data['password2'] = "passwordtest12345"
        invalid_form = UserRegisterForm(data=not_matching_passwords_data)
        self.assertFalse(invalid_form.is_valid())

    def test_creat_user_uppercase_names(self):
        response = self.client.post("/user/register/", data=self.valid_form_data)
        self.assertTrue(User.objects.filter(first_name = "Test").exists())
        self.assertFalse(User.objects.filter(first_name = "test").exists())
        self.assertTrue(User.objects.filter(last_name = "User").exists())
        self.assertFalse(User.objects.filter(last_name = "user").exists())

    def test_user_register_form_bad_first_name(self):
        bad_first_name_data = self.valid_form_data
        bad_first_name_data['first_name'] = "test1"
        invalid_form = UserRegisterForm(data=bad_first_name_data)
        self.assertFalse(invalid_form.is_valid())

    def test_user_register_form_bad_last_name(self):
        bad_last_name_data = self.valid_form_data
        bad_last_name_data['last_name'] = "test1"
        invalid_form = UserRegisterForm(data=bad_last_name_data)
        self.assertFalse(invalid_form.is_valid())
