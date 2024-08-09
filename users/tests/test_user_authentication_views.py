from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.http import Http404

from users.models import Profile


User = get_user_model()

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1234', password='Abc12345')
        self.profile = Profile.objects.create(author=self.user, 
            bio='test bio 123', address='something avenue something')
        
    def test_profile_view_update(self):
        self.client.login(username='testuser1234', password='Abc12345')
        url = reverse('users:profile', kwargs={'id': self.profile.id}) # type: ignore
        form_data = {
            'bio': 'Updated bio',
            'address': 'Updated address',
        }
        response = self.client.post(url, form_data, follow=True)
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertRedirects(response, reverse('users:profile', kwargs={'id': self.profile.id})) # type: ignore
        self.assertContains(response, 'Profile updated successfully.')
        
    def test_profile_view_with_invalid_form(self):
        self.client.login(username='testuser1234', password='Abc12345')
        url = reverse('users:profile', kwargs={'id': self.profile.id}) # type: ignore
        form_data = {
            'bio': '',
            'address': 'a' * 260,
        }
        response = self.client.post(url, form_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error updating profile. Please correct the errors below.')
        self.assertContains(response, 'Ensure this value has at most 255 characters (it has 260).')


class RegistrationViewsTest(TestCase):
    def test_register_view_renders_form(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/register_view.html')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'action="{0}"'.format(reverse('users:register_create')))
        
    def test_register_create_view_with_valid_form(self):
        form_data = {
            'username': 'validusername',
            'email': 'validemail@email.com',
            'password': 'Password1',
            'password2': 'Password1',
            'first_name': 'Valid first name',
            'last_name': 'Valid last name',
        }
        response = self.client.post(reverse('users:register_create'), form_data, follow=True)
        
        self.assertTrue(User.objects.filter(username='validusername').exists())
        self.assertRedirects(response, reverse('users:login'))
        self.assertContains(response, 'Your user has been registered.')
        

class LoginViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUsername', password='Abc12345')
    
    def test_login_view_renders_form(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'action="{0}"'.format(reverse('users:login_create')))
        
    def test_login_create_view_with_valid_credentials(self):
        form_data = {
            'username': 'TestUsername',
            'password': 'Abc12345',
        }
        response = self.client.post(reverse('users:login_create'), form_data, follow=True)
        self.assertRedirects(response, reverse('users:dashboard'))
        self.assertContains(response, 'You are logged in.')
        
    def test_login_with_invalid_credentials(self):
        form_data = {
            'username': 'AnotherUsername',
            'password': 'Def09876',
        }
        response = self.client.post(reverse('users:login_create'), form_data, follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertContains(response, 'Invalid credentials.')
        
    def test_login_create_view_raises_404_if_not_post(self):
        response = self.client.get(reverse('users:login_create'))
        self.assertEqual(response.status_code, 404)
        
    def test_login_with_invalid_username_or_password(self):
        form_data = {
            'username': 'A' * 160,
            'password': 'Def09876',
        }
        response = self.client.post(reverse('users:login_create'), form_data, follow=True)
        
        self.assertRedirects(response, reverse('users:login'))
        self.assertContains(response, 'Invalid username or password.')
        

class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUsername', password='Abc12345')
        self.client.login(username='TestUsername', password='Abc12345')
    
    def test_logout_view_redirects_if_not_post(self):
        response = self.client.get(reverse('users:logout'), follow=True)
        self.assertRedirects(response, reverse('users:login'))
        
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid logout request')
        
    def test_logout_view_with_invalid_user(self):
        response = self.client.post(reverse('users:logout'), {'username': 'InvalidUsername'})
        self.assertRedirects(response, reverse('users:login'))
        
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid logout user')
        
    def test_logout_view_with_valid_request(self):
        response = self.client.post(reverse('users:logout'), {'username': 'TestUsername'}, follow=True)
        self.assertRedirects(response, reverse('users:login'))
        
        messages = list(response.context['messages'])
        self.assertEqual(str(messages[0]), 'Logged out successfully')
