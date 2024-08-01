from django.test import TestCase
from django import forms
from products.models import Product
from users.validators import UserProductValidator
from unittest.mock import patch, call
from decimal import Decimal
from users.forms.product_form import UserProductForm
from collections import defaultdict
from django.core.exceptions import ValidationError


class UserProductFormUnitTest(TestCase):
    def setUp(self):
        self.form_data = {
            'name': 'product name',
            'price': Decimal('55.55'),
            'stock': 25,
            'description': 'product description',
            'cover': None,
        }
        
    def test_user_product_form_init(self):
        form = UserProductForm(data=self.form_data)
        self.assertIsInstance(form._myerrors, defaultdict)
        self.assertEqual(len(form._myerrors), 0)
        
    @patch('users.forms.product_form.UserProductValidator')
    def test_user_product_form_clean(self, mock_validator):
        mock_validator.return_value = None
        form = UserProductForm(data=self.form_data)
        form.is_valid()
        form.clean()
        
        calls = [
            call(self.form_data, ErrorClass=ValidationError)
        ]
        mock_validator.assert_has_calls(calls, any_order=True)
        
    @patch('users.forms.product_form.UserProductValidator')
    def test_user_product_form_clean_with_validation_errors(self, mock_validator):
        mock_validator.side_effect = ValidationError({'name': ['Invalid name']})
        form = UserProductForm(data=self.form_data)
        form.is_valid()
        
        with self.assertRaises(ValidationError):
            form.clean()
