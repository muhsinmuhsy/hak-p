from datetime import datetime, timedelta
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
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + timedelta(minutes=10)

        user = User(
            phone_number=validated_data["phone_number"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY,
            is_customer=True
        )

        user.save()
        send_otp(validated_data["phone_number"], otp)
        return user
