from django.urls import path

from products import views

app_name = 'products'


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    path('<int:pk>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
    path(
        'products/api/',
        views.ProductAPIList.as_view(),
        name='products_api',
    ),
    path(
        'products/api/<int:pk>/',
        views.ProductAPIDetail.as_view(),
        name='products_api_detail',
    ),
    path(
        'products/api/author/<int:pk>/',
        views.ProductsAPIDetailAuthor.as_view(),
        name='products_api_detail_author',
    )
]
