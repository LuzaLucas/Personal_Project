from django import forms
from products.models import Product
from collections import defaultdict
from utils.django_forms import add_attr
from django.core.exceptions import ValidationError
from users.validators import UserProductValidator


class UserProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._myerrors = defaultdict(list)
    
    class Meta:
        model = Product
        fields = 'name', 'price', 'stock', 'description', 'cover'
    
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        UserProductValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean
