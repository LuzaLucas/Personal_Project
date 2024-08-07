from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from django.http import HttpResponse
from unittest.mock import patch

from products.models import Product
from users.views import DashboardProduct
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
    
        products = self.make_product_in_batch(qtd=4)
        
        products[0].author = self.user1
        products[0].is_published = False
        products[0].save()
        
        products[1].author = self.user1
        products[1].save()
        
        products[2].author = self.user2
        products[2].is_published = False
        products[2].save()
        
        products[3].author = self.user2
        products[3].is_published = True
        products[3].save()
        
        self.products = products
        
        self.client.force_login(self.user1)
        
        return super().setUp()
    
    # Dashboard view
    def test_dashboard_view_redirects_if_user_is_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('users:dashboard'))
        self.assertRedirects(response,
            f'{reverse('users:login')}?next={reverse('users:dashboard')}')
        
    def test_dashboard_view_shows_only_unpublished_products_for_logged_user(self):
        response = self.client.get(reverse('users:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('pages/dashboard.html')
        self.assertContains(response, self.products[0])
        self.assertNotContains(response, self.products[1].name)
        self.assertNotContains(response, self.products[2].name)
        
    # DashboardProduct view
    def test_get_product_returns_none_for_published_products(self):
        product_id = self.products[1].pk
        response = self.client.get(reverse('users:dashboard_product_edit', args=[product_id]))
        view = DashboardProduct()
        view.request = response.wsgi_request
        
        product = view.get_product(id=product_id)
        self.assertIsNone(product)
        
    def test_get_product_returns_none_for_other_user_products(self):
        product_id = self.products[2].pk
        response = self.client.get(reverse('users:dashboard_product_edit', args=[product_id]))
        view = DashboardProduct()
        view.request = response.wsgi_request
        
        product = view.get_product(id=product_id)
        self.assertIsNone(product)
        
    def test_get_product_returns_none_if_id_is_none(self):
        response = self.client.get(reverse('users:dashboard_product_create'))
        view = DashboardProduct()
        view.request = response.wsgi_request
        
        product = view.get_product(id=None)
        self.assertIsNone(product)
        
    def test_render_product_renders_correct_template_and_product(self):
        product_id = self.products[0].pk
        response = self.client.get(reverse('users:dashboard_product_edit', args=[product_id]))
        view = DashboardProduct()
        view.request = response.wsgi_request
        
        print(response.content.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertTemplateUsed('pages/dashboard_product.html')
        self.assertContains(response, 'form')
        self.assertIn(self.products[0].name, response.content.decode('utf-8'))
        
    def test_dashboard_product_post(self):
        product_id = self.products[0].pk

        form_data = {
            'name': 'Updated product 0 name',
            'description': 'Updated product 0 description',
            'price': '55.55',
            'stock': '21',
        }

        url = reverse('users:dashboard_product_edit', args=[product_id])
        response = self.client.post(url, data=form_data, follow=True)

        # Print errors in the form (debug only)
        # print("Form errors:", response.context['form'].errors)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard_product.html')
        self.assertContains(response, 'Updated product 0 name')

        product = Product.objects.get(pk=product_id)
        self.assertEqual(product.description, 'Updated product 0 description')
        
    def test_dashboard_product_post_with_invalid_form(self):
        product_id = self.products[0].pk
        
        # Invalid data
        form_data = {
            'name': 'valid name',
            'description': '', # Empty field
            'price': 'not_a_number', # Invalid field
            'stock': '21',
        }
        
        url = reverse('users:dashboard_product_edit', args=[product_id])
        response = self.client.post(url, data=form_data, follow=True)

        form = response.context['form']        
        self.assertTrue(not form.is_valid())
        
        
class DashboardDeleteViewTest(ProductTestBase):
    def setUp(self):
        self.client = Client()
        self.user = self.make_author(
            username='testuser 1234',
            password='testpass',
        )
        self.product = self.make_product(author_data={'username': 'testuser'})
        
    def test_product_delete(self):
        self.client.login(username='testuser 1234', password='testpass')

        self.assertEqual(Product.objects.count(), 1)

        with patch('users.views.dashboard_views.DashboardProductDelete.get_product') as mock_get_product:
            mock_get_product.return_value = self.product

            response = self.client.post(reverse('users:dashboard_product_delete'), {'id': self.product.id}, follow=True) # type: ignore

            self.assertEqual(Product.objects.count(), 0)
            self.assertRedirects(response, reverse('users:dashboard'))
 