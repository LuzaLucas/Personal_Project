from django.urls import reverse, resolve
from django.test import Client
from products.models import Product
from django.contrib.auth.models import User

from users.views import dashboard
from products.tests.test_products_base import ProductTestBase


class DashboardViewsTest(ProductTestBase):
    def setUp(self) -> None:
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='testuser', password='Abc12345',
        )
        self.user2 = User.objects.create_user(
            username='altuser', password='Bcd23456',
        )
    
        products = self.make_product_in_batch(qtd=3)
        products[0].author = self.user1
        products[0].is_published = False
        products[0].save()
        
        products[1].author = self.user1
        products[1].save()
        
        products[2].author = self.user2
        products[2].is_published = False
        products[2].save()
        
        self.products = products
        
        return super().setUp()
    
    def test_dashboard_view_redirects_if_user_is_not_logged_in(self):
        response = self.client.get(reverse('users:dashboard'))
        self.assertRedirects(response,
            f'{reverse('users:login')}?next={reverse('users:dashboard')}')
        
    def test_dashboard_view_shows_only_unpublished_products_for_logged_user(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('users:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/dashboard.html')
        self.assertContains(response, self.products[0])
        self.assertNotContains(response, self.products[1].name)
        self.assertNotContains(response, self.products[2].name)
