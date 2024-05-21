from django.urls import path, include
from admin_app.views import *

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('product/<int:product_id>/view/', ProductViewAPIView.as_view(), name='product-view'),
    path('product/add/', ProductAddAPIView.as_view(), name='product-add'),
    path('colors/', ColorAPIView.as_view(), name='color-api'),
]