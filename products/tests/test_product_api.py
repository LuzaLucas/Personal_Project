from rest_framework.test import APITestCase
from products.tests.test_products_base import ProductMixin
from django.urls import reverse


class ProductAPITtest(APITestCase, ProductMixin):
    def test_product_api_list_return_status_code_200(self):
        api_url = reverse('products:products-api-list')
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)
    
    def test_product_api_list_loads_correct_number_of_products(self):
        wanted_number_of_products = 14
        self.make_product_in_batch(qtd=wanted_number_of_products)
        
        url_page1 = reverse('products:products-api-list')
        response_page1 = self.client.get(url_page1)
        products_loaded1 = len(response_page1.data.get('results'))  # type: ignore
        self.assertEqual(products_loaded1, 10)
        
        url_page2 = f"{reverse('products:products-api-list')}?page=2"
        response_page2 = self.client.get(url_page2)
        products_loaded2 = len(response_page2.data.get('results'))  # type: ignore
        self.assertEqual(products_loaded2, 4)
