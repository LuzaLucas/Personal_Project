from django.test import TestCase
from utils.django_utils_images import resize_image
from PIL import Image
import tempfile
import os


class DjangoUtilsImagesUnitTest(TestCase):
    def setUp(self) -> None:
        self.large_image_path = tempfile.mktemp(suffix='.jpg')
        large_image = Image.new('RGB', (800,800), color=(255, 255, 0))
        large_image.save(self.large_image_path)
        
        self.small_image_path = tempfile.mktemp(suffix='.jpg')
        small_image = Image.new('RGB', (300, 300), color=(165, 165, 165))
        small_image.save(self.small_image_path)
        
        self.rgba_image_path = tempfile.mktemp(suffix='.png')
        rgba_image = Image.new('RGBA', (600,600), color=(213, 212, 211, 210))
        rgba_image.save(self.rgba_image_path)
        
        self.image_paths = [self.large_image_path, self.small_image_path,
            self.rgba_image_path]
        
    def tearDown(self) -> None:
        for image_path in self.image_paths:
            if os.path.exists(image_path):
                os.remove(image_path)
            
    def test_resize_image_func_resizes_images_bigger_than_480px(self):
        resize_image(self.large_image_path)
        with Image.open(self.large_image_path) as image:
            self.assertEqual(image.width, 480)
            self.assertEqual(image.height, round((480 * 800) / 800))
        
    def test_resize_image_func_do_not_resizes_images_smaller_than_480_px(self):
        with Image.open(self.small_image_path) as original_image:
            original_width, original_height = original_image.size
            
        resize_image(self.small_image_path, new_width=480)
        
        with Image.open(self.small_image_path) as resized_image:
            resized_width, resized_height = resized_image.size
        
        self.assertEqual(original_width, resized_width)
        self.assertEqual(original_height, resized_height)
        
    def test_resize_image_func_converts_rgba_to_rgb(self):
        resize_image(self.rgba_image_path)
        with Image.open(self.rgba_image_path) as image:
            self.assertEqual(image.mode, 'RGB')
            self.assertEqual(image.width, 480)
