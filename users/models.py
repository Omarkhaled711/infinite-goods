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

    def full_name(self):
        """
        return the full name of the user
        """
        return f'{self.first_name} {self.last_name}'

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


class UserProfile(models.Model):
    """
    Represents additional profile information for a user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(blank=True, max_length=100)
    profile_image = models.ImageField(
        default='userprofile/default.jpg', upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        """
        Returns a string representation of the UserProfile instance.
        """
        return self.user.first_name
