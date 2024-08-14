from django.urls import path
from rest_framework.routers import SimpleRouter

from products import views

app_name = 'products'
product_api_router = SimpleRouter()
product_api_router.register('products/api', views.ProductAPIViewSet)

print(product_api_router.urls)


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    path('<int:pk>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
    path(
        'products/api/author/<int:pk>/',
        views.ProductsAPIDetailAuthor.as_view(),
        name='products_api_detail_author',
    )
]

urlpatterns += product_api_router.urls
