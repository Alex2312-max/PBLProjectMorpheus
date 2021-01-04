from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from datetime import date
from django.contrib.auth.models import PermissionsMixin
from PBLProject.settings import AUTH_USER_MODEL


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, date, password, bin_data=b'No data'):
        if not email:
            raise ValueError("User name required")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            password=password,
            date=date,
            bin_data=bin_data,
            # weight=weight,
            # height=height,
            # disease=disease,
            # gender=gender,
            # region=region,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            date=date,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# disease = (
#     ('no disease', ' no disease'),
#     ('disease2', 'disease2'),
#     ('disease3', 'disease3'),
#     ('disease4', 'disease4'),)
# gender = (
#     ('M', 'Male'),
#     ('F', 'Female'),)


class user_model(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(verbose_name='email', unique=True)
    date = models.DateField(default=None)
    password = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    bin_data = models.BinaryField(default=b'')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name', 'date']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        # If the full name is not specified, return email
        if self.first_name == "" and self.last_name == "":
            return self.email
        else:
            return self.first_name + " " + self.last_name

    get_full_name.short_description = 'name'

