from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager ## A new class is imported. ##
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True,)

    user_id = models.UUIDField(
        default=uuid4,
        unique=True,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True,
    )

    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female"),
        ("unknown", "unknown"),
    ]
    gender = models.CharField(
        max_length=64,
        choices=GENDER_CHOICES,
        blank=True,
        default="unknown",
        help_text="Gender of the person",
    )
    height = models.FloatField(
        blank=True,
        null=True,
        help_text="Height of the person",
    )
    level = models.FloatField(
        blank=True,
        null=True,
        help_text="Level of the person",
    )
    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Phone number of the person",
    )
    picture = models.CharField(
        max_length=36,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="City of the person",
    )
    state = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="State of the person",
    )
    country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Country of the person",
    )
    dob = models.DateField(
        blank=True,
        null=True,
        help_text="Date of Birth"
    )
    about_me = models.TextField(
        blank=True,
        null=True,
        help_text="about_me"
    )
    active = models.BooleanField(
        default=False
    )
    deleted = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
