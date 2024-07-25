import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from products.models import Product


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
