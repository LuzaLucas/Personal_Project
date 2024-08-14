from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from ..models import Product
from ..serializers import ProductSerializer, AuthorProductSerializer


class ProductAPIViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination


class ProductsAPIDetailAuthor(ListAPIView):
    queryset = Product.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = AuthorProductSerializer
    pagination_class = PageNumberPagination
