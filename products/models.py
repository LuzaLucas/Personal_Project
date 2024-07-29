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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, default=None)

    def __str__(self):
        return self.name
            
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug('name', 'slug')
        
        try:
            this = Product.objects.get(id=self.id) # type: ignore
            if this.cover != self.cover:
                this.cover.delete(save=False)
        except Product.DoesNotExist:
            pass

        super(Product, self).save(*args, **kwargs)

        if self.cover:
            resize_image(self.cover.path, 480)


    def generate_unique_slug(self, field_name, slug_field_name):
        base_slug = slugify(getattr(self, field_name), allow_unicode=True)
        slug = base_slug
        ModelClass = self.__class__
        while ModelClass.objects.filter(**{slug_field_name: slug}).exclude(id=self.id).exists(): # type: ignore
            slug = f"{base_slug}-{random_string(4)}"
        return slug
