from datetime import datetime, timedelta

import jwt
from config import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom Django manager for User model.
    """

    def create_user(self, username, phone_number, password=None):
        """Creates User(phone_number, username, password) and saves it to the database."""
        if username is None:
            raise TypeError("Users must have a username.")

        if phone_number is None:
            raise TypeError("Users must have an phone number.")

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, phone_number, password):
        """Creates superuser User(phone_number, username, password) and saves it to the database"""
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


def phone_number_validator(value):
    if not value.startswith("+7") or not len(value) == 12:
        raise ValueError("Phone number must be in international format: +7XXXXXXXXXX")
    return value


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    phone_number = models.CharField(
        db_index=True,
        unique=True,
        max_length=20,
        null=True,
        blank=True,
        validators=[phone_number_validator],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))}, settings.SECRET_KEY, algorithm="HS256"
        )

        return token
