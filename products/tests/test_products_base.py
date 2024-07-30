from django.test import TestCase

from django.contrib.auth.models import User
from products.models import Category, Product
from decimal import Decimal


class ProductMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
    
    def make_author(
        self,
        first_name='first',
        last_name='last',
        username='nickname',
        password='P@ssw0rd',
        email='email@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
    
    def make_product(
        self,
        name='product name',
        slug='product-name-5k43l',
        price=Decimal('55.55'),
        stock=25,
        description='product description',
        is_published=True,
        author_data=None,
        category_data=None,
    ):
        if author_data is None:
            author_data = {}
        
        if category_data is None:
            category_data = {}
            
        return Product.objects.create(
            name=name,
            slug=slug,
            price=price,
            stock=stock,
            description=description,
            is_published=True,
            author=self.make_author(**author_data),
            category=self.make_category(**category_data),
        )
        
    def make_product_in_batch(self, qtd=6):
        products = []
        for i in range(qtd):
            kwargs = {'name': f'product n{i}', 'slug': f'slug-n-{i}', 'author_data': {'username': f'username-n-{i}'}}
            product = self.make_product(**kwargs)
            products.append(product)
        return products


class ProductTestBase(TestCase, ProductMixin):
    def setUp(self) -> None:
        return super().setUp()
