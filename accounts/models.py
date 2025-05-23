from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)


    is_verified = models.BooleanField(default=False)

    address_line_1 = models.CharField(null=True, blank=True, max_length=100)
    address_line_2 = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    postcode = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    mobile = models.CharField(null=True, blank=True, max_length=15)
    profile_picture = models.ImageField(null=True, blank=True, upload_to="user_profile")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No username, no first_name, last_name

    objects = CustomUserManager()

    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"



class ContactInfo(models.Model):
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    services = models.TextField(help_text="Comma-separated list of services")



    def get_services_list(self):
        return [service.strip() for service in self.services.split(',')]

    def __str__(self):
        return self.company_name
    
class SocialLink(models.Model):
    contact = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='social_links')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Social Links for {self.contact.company_name}"


class LegalPage(models.Model):
    contact = models.OneToOneField(ContactInfo, on_delete=models.CASCADE, related_name='legal_pages')
    terms_url = models.URLField("Terms & Conditions URL", blank=True, null=True)
    privacy_url = models.URLField("Privacy Policy URL", blank=True, null=True)

    def __str__(self):
        return f"Legal Pages for {self.contact.company_name}"