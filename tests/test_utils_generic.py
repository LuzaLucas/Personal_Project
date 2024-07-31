from django.test import TestCase
from utils.django_utils_generic import random_string, generate_upload_path
from unittest.mock import Mock
from datetime import datetime
import os


class DjangoUtilsGenericUnitTest(TestCase):
    def test_utils_random_string_func(self):
        randomstring1 = random_string(4)
        self.assertEqual(len(randomstring1), 4)
        self.assertTrue(randomstring1.isalnum)
        
    
    def test_utils_generate_upload_path_func(self):
        instance_mock = Mock()
        filename = 'example_image.jpg'
        path = generate_upload_path(instance_mock, filename)
        timestamp = datetime.now().strftime("%Y/%m/%d")
        
        self.assertIn('products\\covers\\', path) # windows based pathing
        self.assertIn(timestamp, path)
        self.assertTrue(path.endswith('.jpg'))
        self.assertEqual(len(os.path.basename(path)), 24)
    