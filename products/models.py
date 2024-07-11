from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import string
import random

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    cover = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=110)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            self.slug = f"{base_slug}-{random_string}"
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{self.random_string(4)}'
        return slug

    @staticmethod
    def random_string(length=4):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))
    
