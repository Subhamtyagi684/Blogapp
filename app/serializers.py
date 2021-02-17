from rest_framework import serializers
from .models import Customer, Category, Blog
from rest_framework.serializers import ValidationError
from .validation import *
from django.core.validators import validate_email
from django.contrib.auth import authenticate,login,logout
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist


def validate_category_obj(value):
    obj = Category.objects.filter(name=value)
    if obj:
        return value
    raise APIException("Object with this category name didn't found")


def validate_category_author(value):
    obj = Customer.objects.filter(email=value)
    if obj:
        return value
    raise APIException("Object with this email didn't found")


class UserSerializer(serializers.Serializer):
    
    full_name = serializers.CharField(write_only=True,validators=[validate_name],required=True)
    email = serializers.CharField(write_only=True,validators=[validate_email,UniqueValidator(queryset=Customer.objects.all())],required=True)
    mobile = serializers.CharField(write_only=True,validators=[validate_mobile,UniqueValidator(queryset=Customer.objects.all())],required=True)
    password = serializers.CharField(write_only=True,validators=[validate_password],required=True)

    def save(self):
        full_name = self.validated_data.get('full_name')
        email = self.validated_data.get('email')
        mobile = self.validated_data.get('mobile')
        password = self.validated_data.get('password')

        obj = Customer.objects.create(full_name=full_name,email=email,mobile=mobile)
        obj.set_password(password)
        obj.save()
        return obj


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True)

    def validate(self,data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email,password=password)
        if user is not None:
            return user
        raise APIException('User not found')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
            'name': {
                'validators': [UniqueValidator(queryset=Category.objects.all()),validate_name],
            }
        }


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = ('title','blog','category','author')
        extra_kwargs = {
            'title': {
                'help_text': 'Enter the title of the blog'
            },
            'blog': {
                'help_text': 'Enter your blog here'
            },
            'category': {
                'help_text': 'Enter the primary key id of the existing category'
            },
            'author': {
                'help_text': 'Enter the primary key id of the existing customer'
            }
        }
