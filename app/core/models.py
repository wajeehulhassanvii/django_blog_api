from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
    PermissionsMixin
from phone_field import PhoneField

# for extending django user model we need AbstractBaseUser,
# BaseUserManager -> it will modify how we manage extended User
# and PermissionsMixin


class UserManager(BaseUserManager):
    # **extra_fields means that we take any extra fields passed
    # and now we can pass them them adhoc
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        # self.model will create a new user using emails and
        # any of the extra fields
        user = self.model(email=email, **extra_fields)
        # we save the password as e n crypted, using set_password method
        user.set_password(password)
        # below statement ._db is useful for multiple database
        user.save(using=self._db)
        # now return the created model
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for supporting email as username"""
    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_author = models.BooleanField(default=True)

    # create user manager
    objects = UserManager()

    # now tell the username field to be used
    USERNAME_FIELD = 'email'
