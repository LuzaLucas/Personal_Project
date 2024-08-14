from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination

from ..models import Product
from ..serializers import ProductSerializer, AuthorProductSerializer


class ProductAPIList(ListCreateAPIView):
    queryset = Product.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    
    # def get(self, request):
    #     products = Product.objects.filter(is_published=True).order_by('-created_at')[:10]
    #     serializer = ProductSerializer(
    #         instance=products,
    #         many=True,
    #         context={'request': request},
    #         )
    #     return Response(serializer.data)
        
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     product = serializer.save()
    #     return Response(
    #         ProductSerializer(
    #             product, 
    #             context={'request': request}).data, 
    #             status=status.HTTP_201_CREATED
    #     )


class ProductAPIDetail(APIView):
    def get_product(self, pk):
        product = get_object_or_404(Product.objects.filter(is_published=True), pk=pk)
        return product
        
    def get(self, request, pk):
        product = self.get_product(pk)
        serializer = ProductSerializer(
            instance=product,
            context={'request': request},
            )
        return Response(serializer.data)
        
    def patch(self, request, pk):
        product = self.get_product(pk)
        serializer = ProductSerializer(
            instance=product,
            data=request.data,
            context={'request': request},
            partial=True,
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
    def delete(self, request, pk):
        product = self.get_product(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)     


class ProductsAPIDetailAuthor(APIView):
    serializer_class = AuthorProductSerializer

    def get(self, request, pk):
        products = Product.objects.filter(author_id=pk, is_published=True).order_by('-created_at')
        serializer = self.serializer_class(instance=products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
