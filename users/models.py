'''
Models model for category app
'''

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class ManageUsers(BaseUserManager):
    '''
    Handle user registeration
    '''

    def create_user(self, first_name, last_name, user_name, email, password=None):
        if not user_name:
            raise ValueError("A user name must be provided")
        if not email:
            raise ValueError("An emial must be provided")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, user_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            email=self.normalize_email(email),
            password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Our custom user model
    '''
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    user_name = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=64)

    # some mandatory information required by djanog when
    # creating custom users
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    # login using E-mail
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    objects = ManageUsers()

    def has_perm(self, perm, obj=None):
        '''
        check if the user is an admin who has permissions
        '''
        return self.is_admin

    def has_module_perms(self, add_label):
        '''
        Always return true
        '''
        return True

    def __str__(self):
        '''
        A string representation for the model1
        '''
        return self.email
