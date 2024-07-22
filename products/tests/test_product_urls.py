from django.test import TestCase
from django.urls import reverse


class ProductsURLTest(TestCase):
    def test_products_home_url_is_correct(self):
        url = reverse('products:home')
        self.assertEqual(url, '/')
        
    def test_products_edit_url_is_correct(self):
        url = reverse('products:edit_product', kwargs={'pk': 9})
        self.assertEqual(url, '/9/edit/')
        
    def test_products_delete_url_is_correct(self):
        url = reverse('products:delete_product', kwargs={'pk': 6})
        self.assertEqual(url, '/6/delete/')
