from .test_products_base import ProductTestBase
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.utils.text import slugify
from unittest.mock import patch
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

import os


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
    def tearDown(self):
        # Remove any files created during the tests
        for root, dirs, files in os.walk('media/products/covers/'):
            for file in files:
                os.remove(os.path.join(root, file))   
                  
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
        
    @patch('utils.django_utils_images.resize_image')
    def test_save_without_cover_does_not_call_resize_function(self, mock_resize_image):
        product = self.make_product()
        product.save()
        
        mock_resize_image.assert_not_called()
        
    def test_save_with_cover_calls_resize_image(self):
        image_io = BytesIO()
        image = Image.new('RGB', (800, 800), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        cover_image = SimpleUploadedFile(
            name='cover.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
        
        product = self.make_product(cover=cover_image)
        product.save()
        
        cover_path = product.cover.path
        with Image.open(cover_path) as img:
            self.assertEqual(img.width, 480)
            self.assertEqual(img.height, round((480 * 800) / 800))
        

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
        