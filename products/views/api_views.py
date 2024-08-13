from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

from ..models import Product
from ..serializers import ProductSerializer, AuthorProductSerializer


@api_view(http_method_names=['get', 'post'])
def products_api_list(request):
    
    if request.method == 'GET':
        products = Product.objects.filter(is_published=True).order_by('-created_at')[:10]
        serializer = ProductSerializer(
            instance=products,
            many=True,
            context={'request': request},
            )
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(ProductSerializer(product, context={'request': request}).data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['get', 'patch', 'delete'])
def products_api_detail(request, pk):
    product = get_object_or_404(Product.objects.filter(is_published=True), pk=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(
            instance=product,
            context={'request': request},
            )
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        serializer = ProductSerializer(
            instance=product,
            data=request.data,
            context={'request': request},
            partial=True,
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        


@api_view()
def products_api_detail_author(request, pk):
    products = Product.objects.filter(author_id=pk, is_published=True).order_by('-created_at')
    serializer = AuthorProductSerializer(
        instance=products,
        many=True,
        context={'request': request},
    )
    return Response(serializer.data)