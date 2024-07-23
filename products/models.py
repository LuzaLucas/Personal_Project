from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime
from PIL import Image

import os
import string
import random


def generate_upload_path(instance, filename):
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    timestamp = datetime.now().strftime("%Y/%m/%d")
    new_filename = f"{random_chars}.jpg"
    return os.path.join('products', 'covers', timestamp, new_filename)


class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()
    cover = models.ImageField(upload_to=generate_upload_path, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=110)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            self.slug = f"{base_slug}-{random_string}"

        try:
            this = Product.objects.get(id=self.id) # type: ignore
            if this.cover != self.cover:
                this.cover.delete(save=False)
        except Product.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        if self.cover:
            self.resize_image(self.cover.path, 480)

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

        new_image = image_pillow.resize((new_width, new_height), resample=Image.LANCZOS) # type: ignore

        image_pillow.close()

        new_image.save(
            image_path,
            optimize=True,
            quality=80,
        )


@receiver(post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)
            

@receiver(pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).cover
    except Product.DoesNotExist:
        return False

    if old_file and old_file != instance.cover:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)