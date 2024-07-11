from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

from datetime import datetime
from PIL import Image

import os
import string
import random
import uuid

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
            
        saved = super().save(*args, **kwargs)  # Salvar o objeto Product primeiro
            
        if self.cover:
            self.resize_image(self.cover.path, 480)
            
        return saved  # Retornar o resultado da chamada super().save()

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
    
    @staticmethod
    def resize_image(image_path, new_width=480):
        image_pillow = Image.open(image_path)
        original_width, original_height = image_pillow.size
        
        if original_width <= new_width:
            image_pillow.close()
            return
        
        new_height = round((new_width * original_height) / original_width)
        
        new_image = image_pillow.resize((new_width, new_height), resample=Image.LANCZOS)
        
        # Fechar a imagem original
        image_pillow.close()
        
        # Salvar a nova imagem redimensionada sobrescrevendo a original
        new_image.save(
            image_path,
            optimize=True,
            quality=80,
        )
        
    def generate_filename(self):
        random_chars = uuid.uuid4().hex[:20]
        timestamp = datetime.now().strftime("%Y/%m/%d/%H%M%S")
        return f"{timestamp}__{random_chars}.jpg"