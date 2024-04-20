from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers
from .utils import send_otp

from .models import UserModel



class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.

    Used in POST and GET
    """

    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)

        user = UserModel(
            phone_number=validated_data["phone_number"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY
        )

        user.save()
        send_otp(validated_data["phone_number"], otp)
        return user

