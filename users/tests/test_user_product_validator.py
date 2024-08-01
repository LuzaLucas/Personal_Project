from unittest import TestCase
from django.core.exceptions import ValidationError
from users.validators import UserProductValidator


class TestUserProductValidatorsUnitTest(TestCase):
    def test_product_name_should_be_at_least_5_characters(self):
        data = {
            'name': '1234',
            'description': 'valid description',
        }
        with self.assertRaises(ValidationError) as context:
            UserProductValidator(data)
            
        msg = 'name must have at least 5 characters'
        self.assertIn('name', context.exception.message_dict)
        self.assertIn(msg, context.exception.message_dict['name'])

    def test_product_name_and_description_cannot_be_equal(self):
        data = {
            'name': 'same thing',
            'description': 'same thing',
        }
        with self.assertRaises(ValidationError) as context:
            UserProductValidator(data)
        
        self.assertIn('name', context.exception.message_dict)
        self.assertIn('description', context.exception.message_dict)
            
        msg1 = 'Cannot be equal to description'
        msg2 = 'Cannot be equal to name'
        self.assertIn(msg1, context.exception.message_dict['name'])
        self.assertIn(msg2, context.exception.message_dict['description'])
        
    def test_clean_with_no_errors(self):
        data = {
            'name': 'Valid Name',
            'description': 'Valid description',
        }
        
        try:
            validator = UserProductValidator(data)
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly!")
