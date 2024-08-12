from django.urls import path

from products import views

app_name = 'products'


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    path('<int:pk>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
    path(
        'products/api/',
        views.products_api_list,
        name='products_api',
    ),
    path(
        'products/api/<int:pk>/',
        views.products_api_detail,
        name='products_api_detail',
    ),
    path(
        'products/api/author/<int:pk>/',
        views.products_api_detail_author,
        name='products_api_detail_author',
    )
]
