from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..models import Product
from ..serializers import ProductSerializer


@api_view()
def products_api_list(request):
    products = Product.objects.filter(is_published=True).order_by('-created_at')[:10]
    serializer = ProductSerializer(
        instance=products,
        many=True,
        context={'request': request},
        )
    return Response(serializer.data)


@api_view()
def products_api_detail(request, pk):
    product = get_object_or_404(Product.objects.filter(is_published=True), pk=pk)
    serializer = ProductSerializer(
        instance=product,
        context={'request': request},
        )
    return Response(serializer.data)


@api_view()
def products_api_detail_author(request, pk):
    products = Product.objects.filter(author_id=pk, is_published=True).order_by('-created_at')
    serializer = ProductSerializer(
        instance=products,
        many=True,
        context={'request': request},
    )
    return Response(serializer.data)
