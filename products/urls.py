from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (IndexListView, CreateProductView, UpdateProductView,
    DeleteProductView)


urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('create/', CreateProductView.as_view(), name='create_product'),
    path('<int:pk>/edit/', UpdateProductView.as_view(), name='edit_product'),
    path('<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

