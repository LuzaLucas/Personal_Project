from django.urls import path

from . import views

app_name = 'products'


urlpatterns = [
    path('', views.IndexListView.as_view(), name='home'),
    # path('create/', views.CreateProductView.as_view(), name='create_product'),
    path('<int:pk>/edit/', views.UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', views.DeleteProductView.as_view(), name='delete_product'),
]
