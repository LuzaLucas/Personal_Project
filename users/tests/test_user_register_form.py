from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.urls import reverse

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
        ('username', 'Username must have letters, numbers or some of those @/./+/=/_. The length should be between 4 and 150 characters.'),
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
        
        
class UserRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'username1',
            'first_name': 'firstname1',
            'last_name': 'lastname1',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword',
            'password2': 'Str0ngP@ssword',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('email', 'Email field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
        
    
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'a' * 3
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must have at least 4 characters'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
    
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Username must 150 characters or less'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        
        
    def test_password_field_have_upper_lower_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password must have at least one uppercase letter, one lowercase letter and one number. The length should be at least 8 characters.'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        
    def test_password_and_password2_must_match(self):
        self.form_data['password'] = 'Abc12345'
        self.form_data['password2'] = 'Def12345'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password 2 must match'
        self.assertIn(msg, response.context['form'].errors.get('password'))
