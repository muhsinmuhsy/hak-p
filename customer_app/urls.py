from django.urls import path, include
from customer_app.views import *

urlpatterns = [
     path('category/list/', CategoryListView.as_view(), name='category-list'),
     path('product/with/variants/list/', ProductWithVariantsList.as_view(), name='product-with-variants-list'),
]