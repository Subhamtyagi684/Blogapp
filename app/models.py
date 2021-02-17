from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .validation import *
from django.core.validators import validate_email,validate_integer
import random
from datetime import date,datetime
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, full_name, email, mobile, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not full_name:
            raise ValueError('Users must provide a name')
        if not mobile:
            raise ValueError('Users must have a mobile number')
        if len(str(password))<5:
            raise ValueError('Minimum length of the password should 5 characters')
        if str(password).isdigit()==True:
            raise ValueError('At lease one alphabet is required')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            mobile=mobile
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, full_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            full_name=full_name,
            mobile=mobile,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Customer(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        validators=[validate_email]
    )
    full_name = models.CharField(max_length=150, validators=[validate_name])
    mobile=models.CharField(max_length=10, validators=[validate_mobile],unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Category(models.Model):
    name = models.CharField(max_length=255,blank=False,null=False,validators=[validate_name],help_text='Ensure this field have only alphabets and minimum length should be 2 characters ',unique=True)

    def __str__(self):
        return self.name
    

class Blog(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=False,null=False,unique=True)
    blog = models.TextField(max_length=2055,blank=False,null=False,unique=True)
    author = models.ForeignKey(Customer,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    