from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from utils.django_utils_generic import generate_upload_path, random_string
from utils.django_utils_images import resize_image


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
        blank=True, default=None)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = f"{base_slug}-{random_string(4)}"

        try:
            this = Product.objects.get(id=self.id) # type: ignore
            if this.cover != self.cover:
                this.cover.delete(save=False)
        except Product.DoesNotExist:
            pass

        super().save(*args, **kwargs)

        if self.cover:
            resize_image(self.cover.path, 480)

    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        while Product.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{random_string(4)}'
        return slug
