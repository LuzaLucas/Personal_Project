from rest_framework import serializers
from .models import Product, Category
from users.validators import UserProductValidator


class ProductSerializer(serializers.ModelSerializer):
    public = serializers.BooleanField(source='is_published', read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author_links = serializers.HyperlinkedRelatedField(
        many=False,
        source='author',
        view_name='products:products_api_detail_author',
        read_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'price', 'description', 'public', 
                  'category', 'author', 'author_links']
    
    def validate(self, attrs):
        UserProductValidator(data=attrs, ErrorClass=serializers.ValidationError)
        return super().validate(attrs)
    
    def create(self, validated_data):
        author = validated_data.pop('author')
        product = Product.objects.create(author=author, **validated_data)
        return product
    

class AuthorProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    stock = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    public = serializers.BooleanField(source='is_published')
    category = serializers.StringRelatedField()
    