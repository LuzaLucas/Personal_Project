from rest_framework import serializers
from django.contrib.auth.models import User


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    stock = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    description = serializers.CharField()
    public = serializers.BooleanField(source='is_published')
    category = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    author_links = serializers.HyperlinkedRelatedField(
        many=False,
        source='author',
        queryset=User.objects.all(),
        view_name='products:products_api_detail_author'
    )
    