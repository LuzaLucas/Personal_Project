from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from products import views

app_name = 'products'
product_api_router = SimpleRouter()
product_api_router.register('products/api', views.ProductAPIViewSet, 
    basename='products-api')


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    path('<int:pk>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
    path(
        'products/api/author/<int:pk>/',
        views.ProductsAPIDetailAuthor.as_view(),
        name='products_api_detail_author',
    ),
    path(
        'products/api/me/',
        views.LoggedInUserAPIView.as_view(),
        name='products_api_me',
    ),
    path(
        'products/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'products/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'products/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify',
    ),
]

urlpatterns += product_api_router.urls
