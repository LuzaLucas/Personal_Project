from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Product
from .permissions import IsOwner
from ..serializers import ProductSerializer, AuthorProductSerializer


class ProductAPIViewSet(ModelViewSet):
    queryset = Product.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(
            Product.objects.filter(is_published=True).order_by('-created_at'),
            pk=pk
        )
        
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return[IsOwner(),]
        
        return super().get_permissions()


class ProductsAPIDetailAuthor(ListAPIView):
    queryset = Product.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = AuthorProductSerializer
    pagination_class = PageNumberPagination
