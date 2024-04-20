from django.urls import path, include
from auth_app.views import UserViewSet
from rest_framework.routers import DefaultRouter
from auth_app.views import *

# Create a router and register the UserViewSet with it
router = DefaultRouter()
router.register("user", UserViewSet, basename="user")

# The generated URLs for the UserViewSet will include routes for list, create, retrieve, update, partial_update, and destroy actions.

urlpatterns = [
    path("", include(router.urls)),  # Include the generated URLs from the router
    path('current_user/', CurrentUser.as_view(), name='current_user'),
    
]


# urlpatterns = [
#     path('user/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user'),
#     path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
#     path('user/<int:pk>/verify-otp/', UserViewSet.as_view({'patch': 'verify_otp'}), name='user-verify-otp'),
#     path('user/<int:pk>/regenerate-otp/', UserViewSet.as_view({'patch': 'regenerate_otp'}), name='user-regenerate-otp'),
# ]