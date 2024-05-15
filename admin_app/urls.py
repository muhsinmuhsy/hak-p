from django.urls import path, include
from admin_app.views import *

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
]