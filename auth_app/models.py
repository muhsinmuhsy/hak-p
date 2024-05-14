from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, validate_email
from django.db import models

phone_regex = RegexValidator(
    regex=r"^\d{10}$", message="Phone number must be 10 digits only."
)

class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given username or email and password.
        """
        if not (username or email):
            raise ValueError("Either username or email is required.")
        email = self.normalize_email(email) if email else None
        username = self.model.normalize_username(username) if username else None
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username or email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username=username, email=email, phone_number=phone_number, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """

    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True, null=True, blank=True, validators=[validate_email])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)
    is_customer = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, null=True, blank=True, validators=[phone_regex])
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(null=True, blank=True)
    
    is_product_admin = models.BooleanField(default=False)
    is_order_admin = models.BooleanField(default=False)
    is_sales_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username or f"User ID: {self.id}"
    
    

class UserProfile(models.Model):
    """
    User profile model.

    Every user should have only one profile.
    """

    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    # address = models.CharField(max_length=100, null=False, blank=False)


# from django.conf import settings
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     BaseUserManager,
#     Group,
#     PermissionsMixin,
# )
# from django.core.validators import RegexValidator, validate_email
# from django.db import models


# phone_regex = RegexValidator(
#     regex=r"^\d{10}", message="Phone number must be 10 digits only."
# )


# class UserManager(BaseUserManager):
#     """
#     User Manager.
#     To create superuser.
#     """

#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('The username field must be set')
#         username = self.model.normalize_username(username)
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, password, **extra_fields)
    
    


# class User(AbstractBaseUser, PermissionsMixin):
#     """
#     Custom User model.
#     """
    
#     username = models.CharField(
#         unique=True, max_length=50, null=True, blank=True)
    
#     email = models.EmailField(
#         max_length=50,
#         blank=True,
#         null=True,
#         validators=[validate_email],
#     )
    
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     user_registered_at = models.DateTimeField(auto_now_add=True)

#     is_customer = models.BooleanField(default=False)

#     phone_number = models.CharField(
#         unique=True, max_length=10, null=True, blank=True, validators=[phone_regex]
#     )

#     otp = models.CharField(max_length=6)
#     otp_expiry = models.DateTimeField(blank=True, null=True)
#     max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
#     otp_max_out = models.DateTimeField(blank=True, null=True)

#     USERNAME_FIELD = "username"

#     objects = UserManager()

#     def __str__(self):
#         return self.username or "User ID: {}".format(self.pk)



# class UserProfile(models.Model):
#     """
#     User profile model.

#     Every user should have only one profile.
#     """

#     user = models.OneToOneField(
#         UserModel,
#         related_name="profile",
#         on_delete=models.CASCADE,
#         primary_key=True,
#     )
#     first_name = models.CharField(max_length=50, null=False, blank=False)
#     last_name = models.CharField(max_length=50, null=False, blank=False)
#     address = models.TextField(null=False, blank=False)