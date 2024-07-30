from django.test import TestCase
from parameterized import parameterized

from users.forms.register_form import RegisterForm
from users.forms.login import LoginForm


class UserRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username goes here'),
        ('email', 'Your email goes here'),
        ('first_name', 'Your first name goes here'),
        ('last_name', 'Your last name goes here'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password here'),
    ])
    def test_fields_placeholder_is_correct_in_register_form(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)
        

    @parameterized.expand([
        ('username', 'Username must have letters, number or some of those @/./+/=/_. The length should be between 4 and 150 characters.'),
        ('email', 'The email must be valid'),
        ('password', 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_helptext = form[field].field.help_text
        self.assertEqual(help_text, current_helptext)
        
        
    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'Email'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(label, current_label)
        

class UserLoginFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type your username'),
        ('password', 'Type your password'),
    ])
    def test_fields_placeholder_is_correct_in_login_form(self, field, placeholder):
        form = LoginForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)
