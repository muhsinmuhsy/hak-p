from django.urls import path, include
from auth_app.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('customer/', CustomerListCreate.as_view(), name='user-list-create'),
    path('customer/<int:customer_id>/', CustomerDetail.as_view(), name='user-detail'),
    path('customer/<int:customer_id>/verify-otp/', CustomerVerifyOTP.as_view(), name='user-verify-otp'),
    path('customer/<int:customer_id>/regenerate-otp/', CustomerRegenerateOTP.as_view(), name='user-regenerate-otp'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('user/customer/profile/add/', UserProfileGetAdd.as_view()),
    
    path('product-admins/', ProductAdminListCreate.as_view(), name='product_admin_list_create'),
    
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
]


# urlpatterns = [
#     path('user/', CustomerViewSet.as_view({'get': 'list', 'post': 'create'}), name='user'),
#     path('user/<int:pk>/', CustomerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
#     path('user/<int:pk>/verify-otp/', CustomerViewSet.as_view({'patch': 'verify_otp'}), name='user-verify-otp'),
#     path('user/<int:pk>/regenerate-otp/', CustomerViewSet.as_view({'patch': 'regenerate_otp'}), name='user-regenerate-otp'),
# ]