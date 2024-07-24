from .test_products_base import ProductTestBase
from django.core.exceptions import ValidationError
from decimal import Decimal

from products.models import Category


class ProductModelTest(ProductTestBase):
    def setUp(self) -> None:
        self.product = self.make_product()
        return super().setUp()
            
    def test_product_name_max_length(self):
        self.product.name = 'A' * 101

        with self.assertRaises(ValidationError) as cm:
            self.product.full_clean()

    def test_product_price_max_length(self):
        self.product.price = Decimal('1234567.89')

        with self.assertRaises(ValidationError):
            self.product.full_clean()


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
        