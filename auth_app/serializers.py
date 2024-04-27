from datetime import timedelta
import random
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from .models import User
from .utils import send_otp

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model used in POST and GET requests.
    """

    class Meta:
        model = User
        fields = ("id", "phone_number")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """
        Method to create a new user with OTP verification.
        """
        phone_number = validated_data["phone_number"]

        if User.objects.filter(phone_number=phone_number, is_active=True).exists():
            # If phone number already exists, update existing user's OTP
            user = User.objects.get(phone_number=phone_number)
            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + timedelta(minutes=10)
            
            user.otp = otp
            user.otp_expiry = otp_expiry
            user.max_otp_try = settings.MAX_OTP_TRY
            user.is_customer = True
            user.save()

            send_otp(phone_number, otp)

            return user
        else:
            # If phone number doesn't exist, create a new user
            otp = random.randint(1000, 9999)
            otp_expiry = timezone.now() + timedelta(minutes=10)

            user = User.objects.create(
                phone_number=phone_number,
                otp=otp,
                otp_expiry=otp_expiry,
                max_otp_try=settings.MAX_OTP_TRY,
                is_customer=True
            )

            send_otp(phone_number, otp)

            return user



# from datetime import datetime, timedelta
# import random
# from django.conf import settings
# from django.utils import timezone
# from rest_framework import serializers
# from .models import User
# from .utils import send_otp

# class CustomerSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the User model used in POST and GET requests.
#     """

#     class Meta:
#         model = User
#         fields = ("id", "phone_number")
#         read_only_fields = ("id",)

#     def create(self, validated_data):
#         """
#         Method to create a new user with OTP verification.
#         """
#         otp = random.randint(1000, 9999)
#         otp_expiry = timezone.now() + timedelta(minutes=10)

#         user = User(
#             phone_number=validated_data["phone_number"],
#             otp=otp,
#             otp_expiry=otp_expiry,
#             max_otp_try=settings.MAX_OTP_TRY,
#             is_customer=True
#         )

#         user.save()
#         send_otp(validated_data["phone_number"], otp)
#         return user
