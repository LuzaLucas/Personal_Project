from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Profile
from users.forms.profile_form import ProfileForm


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
