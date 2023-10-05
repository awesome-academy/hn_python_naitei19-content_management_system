from django.test import TestCase
from home.forms import RegisterForm
from home.forms import UserForm
from home.models import User

class TestRegisterForm(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': "valid_username",
            'email': 'example@example.com',
            'password1': '12password123',
            'password2': '12password123',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        form_data = {
            'username': "",
            'email': 'example@example.com',
            'password1': '123password123',
            'password2': '123password123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

     # Đây là một email không hợp lệ
    def test_invalid_email(self):
        form_data = {
            'username': "valid_username",
            'email': 'invalid_email', 
            'password1': '123password123',
            'password2': '123password123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_duplicate_username(self):
        # Tạo một người dùng có cùng username trước đó
        User.objects.create_user(username="existing_user", password="password123")
        form_data = {
            'username': "existing_user",  
            'email': 'new@example.com',
            'password1': 'new_password123',
            'password2': 'new_password123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    # Password2 không khớp với Password1
    def test_password_mismatch(self):
        form_data = {
            'username': "valid_username",
            'email': 'example@example.com',
            'password1': 'password123',
            'password2': 'mismatched_password',  
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_short_password(self):
        form_data = {
            'username': "valid_username",
            'email': 'example@example.com',
            'password1': 'short',
            'password2': 'short',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn("This password is too short. It must contain at least 8 characters.", form.errors['password2'])

    def test_common_password(self):
        form_data = {
            'username': "valid_username",
            'email': 'example@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn("This password is too common.", form.errors['password2'])

    def test_numeric_password(self):
        form_data = {
            'username': "valid_username",
            'email': 'example@example.com',
            'password1': '12345678',
            'password2': '12345678',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        self.assertIn("This password is entirely numeric.", form.errors['password2'])

class TestEditForm(TestCase):
    def setUp(self):
        self.form_data = {
             'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'username': 'johndoe123'
        }
        
    def test_valid_form(self):
        form = UserForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = UserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_invalid_email(self):
        invalid_email_data = self.form_data.copy()
        invalid_email_data['email'] = 'invalid_email'
        form = UserForm(data=invalid_email_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
