from django.urls import path, include
from customer_app.views import *

urlpatterns = [
     path('category/list/', CategoryListView.as_view(), name='category-list'),
     path('category/<int:category_id>/with/variants/', CategoryWithProducts.as_view(), name='category-with-variants'),
     
     path('product/with/variants/', ProductWithVariants.as_view(), name='product-with-variants-list'),
     
]