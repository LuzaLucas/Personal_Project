from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="register_create"),
    path('login/', views.login_view, name="login"),
    path('login/create/', views.login_create, name="login_create"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/<int:id>/', views.ProfileView.as_view(), name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/product/new', views.DashboardProduct.as_view(), name="dashboard_product_create"),
    path('dashboard/product/delete', views.DashboardProductDelete.as_view(), name="dashboard_product_delete"),
    path('dashboard/product/<int:id>/edit/', views.DashboardProduct.as_view(), name="dashboard_product_edit"),
]
