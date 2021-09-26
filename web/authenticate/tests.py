from django.test import TestCase
from .forms import UserRegisterForm
from django.contrib.auth.models import User

class UserRegisterFormTests(TestCase):
    def test_create_user_success(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertTrue(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_missing_username(self):
        form_data = {"first_name": "test", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())
    
    def test_create_user_missing_first_name(self):
        form_data = {"username": "NewTestUser", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_missing_last_name(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_missing_email(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_missing_password1(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "email": "testing@test.no", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_missing_password2(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_create_user_password_not_matching(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest12345"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertFalse(User.objects.filter(username = "NewTestUser").exists())

    def test_uppercase_names(self):
        form_data = {"username": "NewTestUser", "first_name": "test", "last_name": "user", "email": "testing@test.no", "password1": "passwordtest1234", "password2": "passwordtest1234"}
        response = self.client.post("/authenticate/register/", data=form_data)
        self.assertTrue(User.objects.filter(first_name = "Test").exists())
        self.assertFalse(User.objects.filter(first_name = "test").exists())
        self.assertTrue(User.objects.filter(last_name = "User").exists())
        self.assertFalse(User.objects.filter(last_name = "user").exists())
