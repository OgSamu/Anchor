from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
import uuid
from django.contrib.auth.models import Group, Permission


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("A username is required.")
        if not password:
            raise ValueError("A password is required.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_superuser = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=140, unique=True)

    # url link to user profile
    url = models.URLField(blank=True, null=True, editable=False)
    profileImage = models.URLField(blank=True, null=True)
    displayName = models.CharField(max_length=100, blank=True, null=True)

    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed_by", blank=True
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="follows", blank=True
    )

    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name="app_users", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="app_users", blank=True
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return (
            f"{self.username} ({self.displayName})"
            if self.displayName
            else self.username
        )
