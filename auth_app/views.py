from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from .models import User, UserProfile
from .serializers import CustomerSerializer, UserProfileSerializer, AdminSerializer
from .utils import send_otp
import random
import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate, login



# class CustomerListCreate(APIView):
#     def get(self, request, format=None):
#         try:
#             # Retrieve customers who are flagged as 'customer'
#             users = User.objects.filter(is_customer=True)
#             if not users:
#                 return Response({"message": "The customer is empty"})
#             serializer = CustomerSerializer(users, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             # Handle specific exceptions if necessary
#             return Response({"error": "Failed to retrieve customers"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, format=None):
#         try:
#             serializer = CustomerSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # Provide specific error messages for different validation failures
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             # Handle specific exceptions if necessary
#             return Response({"error": "Failed to create customer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerListCreate(APIView):
    def get(self, request, format=None):
        try:
            # Retrieve customers who are flagged as 'customer'
            users = User.objects.filter(is_customer=True)
            if not users:
                return Response({"message": "The customer is empty"})
            serializer = CustomerSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve customers: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Provide specific error messages for different validation failures
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create customer: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerDetail(APIView):
    def get_object(self, customer_id):
        return get_object_or_404(User, id=customer_id)

    def get(self, request, customer_id, format=None):
        try:
            user = self.get_object(customer_id)
            serializer = CustomerSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

    def put(self, request, customer_id, format=None):
        try:
            user = self.get_object(customer_id)
            serializer = CustomerSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, customer_id, format=None):
        try:
            user = self.get_object(customer_id)
            serializer = CustomerSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, customer_id, format=None):
        try:
            user = self.get_object(customer_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerVerifyOTP(APIView):
    def patch(self, request, customer_id=None, format=None):
        try:
            user = get_object_or_404(User, id=customer_id)
            otp = request.data.get("otp")

            if user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # User is already active, update OTP-related fields and generate token
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp' : 'Successfully verified the customer',
                    'message' : 'The customer already exists'
                }
                return Response(data, status=status.HTTP_200_OK)

            elif not user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
                # OTP verification successful, activate user and generate token
                user.is_active = True
                user.otp_expiry = None
                user.max_otp_try = settings.MAX_OTP_TRY
                user.otp_max_out = None
                user.save()

                refresh = RefreshToken.for_user(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'otp' : 'Successfully verified the customer',
                    'message' : 'New customer'
                }
                return Response(data,  status=status.HTTP_201_CREATED)
            else:
                return Response("incorrect OTP.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Something went wrong: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CustomerRegenerateOTP(APIView):
    def patch(self, request, customer_id=None, format=None):
        try:
            user = get_object_or_404(User, id=customer_id)

            if int(user.max_otp_try) == 0 and timezone.now() < user.otp_max_out:
                return Response(
                    "Max OTP try reached, try after an hour",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
            max_otp_try = int(user.max_otp_try) - 1

            user.otp = otp
            user.otp_expiry = otp_expiry
            user.max_otp_try = max_otp_try

            if max_otp_try == 0:
                otp_max_out = timezone.now() + datetime.timedelta(hours=1)
                user.otp_max_out = otp_max_out
            elif max_otp_try == -1:
                user.max_otp_try = settings.MAX_OTP_TRY
            else:
                user.otp_max_out = None
                user.max_otp_try = max_otp_try

            user.save()
            send_otp(user.phone_number, otp)
            return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class UserProfileGetAdd(APIView):
      
#     def post(self, request, customer_id=None, format=None):
#         try:
#             user = get_object_or_404(User, id=customer_id, is_customer=True)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        
#         first_name = request.data.get('first_name')
#         last_name = request.data.get('last_name')
#         user_profile = UserProfile.objects.create(
#             user=user,
#             first_name=first_name,
#             last_name=last_name
#             )
#         user_profile_serializer = UserProfileSerializer(user_profile)
#         return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
class UserProfileGetAdd(APIView):
    def post(self, request, format=None):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        user = request.user
        try:
            user_profile = UserProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name
            )
            user_profile_serializer = UserProfileSerializer(user_profile)
            return Response(user_profile_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        

# @permission_classes([IsAuthenticated])
# class DashboardView(APIView):
#     def get(self, request):
#         try:
#             response = f"Hey {request.user}, You are seeing a Get response"
#             return Response({'response': response}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request):
#         try:
#             text = request.data.get("text")
#             if text is None:
#                 return Response({'error': 'Text is required'}, status=status.HTTP_400_BAD_REQUEST)
#             response = f"Hey {request.user}, Your text is {text}"
#             return Response({'response': response}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## ---------------------------------------------------------------------------------------------------------##



class ProductAdminListCreate(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.filter(is_product_admin=True)
            if not users:
                return Response({"message": "No product admins found."}, status=status.HTTP_204_NO_CONTENT)
            serializer = AdminSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve product admins: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_product_admin=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create product admin: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# {
#     "username": "exameOOple_user",
#     "password": "password",
#     "email": "admin@example.com",
#     "phone_number": "1234567890",
#     "first_name": "John",
#     "last_name": "Doe"
# }


class OrderAdminListCreate(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.filter(is_order_admin=True)
            if not users:
                return Response({"message": "No Order admins found."}, status=status.HTTP_204_NO_CONTENT)
            serializer = AdminSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve Order admins: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_order_admin=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create product admin: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        

class SalesAdminListCreate(APIView):
    def get(self, request, format=None):
        try:
            users = User.objects.filter(is_sales_admin=True)
            if not users:
                return Response({"message": "No Sales admins found."}, status=status.HTTP_204_NO_CONTENT)
            serializer = AdminSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to retrieve Sales admins: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = AdminSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_sales_admin=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Failed to create sales admin: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message' : 'Login successful'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": "An error occurred during login", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from django.conf import settings
# from .models import User
# from .serializers import CustomerSerializer
# from .utils import send_otp
# import random
# import datetime
# from rest_framework_simplejwt.tokens import RefreshToken

# # Create your views here.

# class CustomerListCreate(APIView):
#     def get(self, request):
#         users = User.objects.all()
#         serializer = CustomerSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class CustomerDetail(APIView):
#     def get_object(self, customer_id):
#         return get_object_or_404(User, id=customer_id)

#     def get(self, request, customer_id):
#         user = self.get_object(customer_id)
#         serializer = CustomerSerializer(user)
#         return Response(serializer.data)

#     def put(self, request, customer_id):
#         user = self.get_object(customer_id)
#         serializer = CustomerSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, customer_id):
#         user = self.get_object(customer_id)
#         serializer = CustomerSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, customer_id):
#         user = self.get_object(customer_id)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class CustomerVerifyOTP(APIView):
#     def patch(self, request, customer_id=None):
#         user = get_object_or_404(User, id=customer_id)
#         otp = request.data.get("otp")

#         if not user.is_active and user.otp == otp and user.otp_expiry and timezone.now() < user.otp_expiry:
#             user.is_active = True
#             user.otp_expiry = None
#             user.max_otp_try = settings.MAX_OTP_TRY
#             user.otp_max_out = None
#             user.save()

#             refresh = RefreshToken.for_user(user)
#             data = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'otp' : 'Successfully verified the user'
#             }
#             return Response(data,  status=status.HTTP_200_OK)
#         else:
#             return Response(
#                 "User active or Please enter the correct OTP.",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

# class CustomerRegenerateOTP(APIView):
#     def patch(self, request, customer_id=None):
#         user = get_object_or_404(User, id=customer_id)

#         if int(user.max_otp_try) == 0 and timezone.now() < user.otp_max_out:
#             return Response(
#                 "Max OTP try reached, try after an hour",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         otp = random.randint(1000, 9999)
#         otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#         max_otp_try = int(user.max_otp_try) - 1

#         user.otp = otp
#         user.otp_expiry = otp_expiry
#         user.max_otp_try = max_otp_try

#         if max_otp_try == 0:
#             otp_max_out = timezone.now() + datetime.timedelta(hours=1)
#             user.otp_max_out = otp_max_out
#         elif max_otp_try == -1:
#             user.max_otp_try = settings.MAX_OTP_TRY
#         else:
#             user.otp_max_out = None
#             user.max_otp_try = max_otp_try

#         user.save()
#         send_otp(user.phone_number, otp)
#         return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)




# import datetime
# import random

# from django.conf import settings
# from django.utils import timezone
# from rest_framework import status, viewsets 
# from rest_framework.decorators import action
# from rest_framework.response import Response

# from .utils import send_otp

# from .models import User
# from .serializers import CustomerSerializer

# from rest_framework_simplejwt.tokens import RefreshToken


# class CustomerViewSet(viewsets.ModelViewSet):
#     """
#     UserModel View.
#     """

#     queryset = User.objects.all()
#     serializer_class = CustomerSerializer

#     @action(detail=True, methods=["PATCH"])
#     def verify_otp(self, request, pk=None):
#         instance = self.get_object()
#         if (
#             not instance.is_active
#             and instance.otp == request.data.get("otp")
#             and instance.otp_expiry
#             and timezone.now() < instance.otp_expiry
#         ):
#             instance.is_active = True
#             instance.otp_expiry = None
#             instance.max_otp_try = settings.MAX_OTP_TRY
#             instance.otp_max_out = None
#             instance.save()

#             # Generate JWT token
#             refresh = RefreshToken.for_user(instance)
#             data = {
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'otp' : 'Successfully verified the user'
#             }
#             return Response(data,  status=status.HTTP_200_OK)
#             # return Response(
#             #     "Successfully verified the user.", status=status.HTTP_200_OK
#             # )

#         return Response(
#             "User active or Please enter the correct OTP.",
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#     @action(detail=True, methods=["PATCH"])
#     def regenerate_otp(self, request, pk=None):
#         """
#         Regenerate OTP for the given user and send it to the user.
#         """
#         instance = self.get_object()
#         if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
#             return Response(
#                 "Max OTP try reached, try after an hour",
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         otp = random.randint(1000, 9999)
#         otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#         max_otp_try = int(instance.max_otp_try) - 1

#         instance.otp = otp
#         instance.otp_expiry = otp_expiry
#         instance.max_otp_try = max_otp_try
#         if max_otp_try == 0:
#             # Set cool down time
#             otp_max_out = timezone.now() + datetime.timedelta(hours=1)
#             instance.otp_max_out = otp_max_out
#         elif max_otp_try == -1:
#             instance.max_otp_try = settings.MAX_OTP_TRY
#         else:
#             instance.otp_max_out = None
#             instance.max_otp_try = max_otp_try
#         instance.save()
#         send_otp(instance.phone_number, otp)
#         return Response("Successfully generate new OTP.", status=status.HTTP_200_OK)

