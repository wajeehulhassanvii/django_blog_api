from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
    PermissionsMixin
from phone_field import PhoneField

# the recommended way of retrieving different settings from django
# settings file
from django.conf import settings

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
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # we save the password as e n crypted, using set_password method
        user.set_password(password)
        # below statement ._db is useful for multiple database
        user.save(using=self._db)
        # now return the created model
        return user

    def create_superuser(self, email, password):
        """Create and save new superuser.\
            We will create superuser from command line so we\
            don\'t care about extra parameters """
        # NOTE: we are using create_user method from above
        # for creating the superuser with email only
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

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


class Tag(models.Model):
    """Tag to be used for blog"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        # model we wannta base foreign key off
        settings.AUTH_USER_MODEL,
        # we specify what happens when we delete user
        # we would delete the tags as the user itself gets deleted
        on_delete=models.CASCADE
    )

    def __str__(self):
        """return toString or str(obj)"""
        return self.name
