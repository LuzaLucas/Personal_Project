from django.urls import reverse, resolve
from decimal import Decimal

from products.views import product_views
from .test_products_base import ProductTestBase
  

class ProductsViewsTest(ProductTestBase):
    # home view
    def test_products_home_view_is_correct(self):
        view = resolve(reverse('products:home'))
        self.assertIs(view.func.view_class, product_views.IndexListView)
        
    def test_products_home_view_returns_status_code_200_if_ok(self):
        response = self.client.get(reverse('products:home'))
        self.assertEqual(response.status_code, 200)
        
    def test_products_home_view_loads_correct_template(self):
        response = self.client.get(reverse('products:home'))
        self.assertTemplateUsed(response, 'index.html')
        
    def test_products_home_template_shows_no_products_found_if_no_products(self):
        response = self.client.get(reverse('products:home'))
        self.assertIn('No products have been added yet.', response.content.decode('utf-8'))
        
    def test_products_home_template_loads_products(self):
        self.make_product()
        response = self.client.get(reverse('products:home'))
        content = response.content.decode('utf-8')
        self.assertIn('product name', content)
        
        response_product = response.context['product_list']
        self.assertEqual(25, response_product.first().stock)
    
    # update view
    def test_products_update_view_is_correct(self):
        view = resolve(reverse('products:edit_product', kwargs={'pk': 5}))
        self.assertIs(view.func.view_class, product_views.UpdateProductView)
        
    def test_form_valid_updates_is_published(self):
        product = self.make_product()
        
        data = {
            'name': 'updated name',
            'stock': 10,
            'price': 44.99,
            'description': 'updated description',
        }

        url = reverse('products:edit_product', kwargs={'pk': product.pk})
        response = self.client.post(url, data)

        product.refresh_from_db()

        self.assertFalse(product.is_published)
        self.assertRedirects(response, reverse('products:home'))

        self.assertEqual(product.name, 'updated name')
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.price, Decimal('44.99'))
        self.assertEqual(product.description, 'updated description')
        
    # delete view
    def test_products_delete_view_is_correct(self):
        view = resolve(reverse('products:delete_product', kwargs={'pk': 5}))
        self.assertIs(view.func.view_class, product_views.DeleteProductView)
    
