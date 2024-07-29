from .test_products_base import ProductTestBase
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.text import slugify
from django.core.management import call_command

from utils.django_utils_generic import random_string
from products.models import Product


class ProductModelTest(ProductTestBase):
    def setUp(self) -> None:
        self.product = self.make_product()
        return super().setUp()
    
    def test_product_model_string_representation_is_name_field(self):
        self.assertEqual(str(self.product), self.product.name)
            
    def test_product_name_max_length(self):
        self.product.name = 'A' * 101

        with self.assertRaises(ValidationError) as cm:
            self.product.full_clean()

    def test_product_price_max_length(self):
        self.product.price = Decimal('1234567.89')

        with self.assertRaises(ValidationError):
            self.product.full_clean()
    
    
class ProductModelSaveTest(ProductTestBase):        
    def test_product_slug_is_generated_if_not_provided(self):
        product = self.make_product(slug='')
        product.save()
        self.assertIsNotNone(product.slug)
        
    def test_product_slug_is_not_changed_on_update(self):
        product = self.make_product()
        original_slug = product.slug
        product.name = 'Updated product name'
        product.save()
        self.assertEqual(product.slug, original_slug)
        
    def test_product_model_generates_unique_slug(self):
        product1 = self.make_product(
            name='Unique Product Name',
            slug='',
            author_data={
                'username':'another user'
            })
        product1.save()
        
        product2 = self.make_product(
            name='Another unique Product Name',
            slug='',
        )
        product2.save()
        
        self.assertNotEqual(product1.slug, product2.slug)
        expected_slug_start = slugify(product2.name)
        self.assertTrue(product2.slug.startswith(expected_slug_start))


class CategoryModelTest(ProductTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category testing'
        )
        return super().setUp()
    
    def test_category_model_string_representation_is_name_field(self):
        self.assertEqual(str(self.category), self.category.name)
        
    def test_category_name_max_length(self):
        self.category.name = 'A' * 51
        with self.assertRaises(ValidationError):
            self.category.full_clean()
        