from django.db import models
from django.db.models import fields
from api.utils import Util
from rest_framework import serializers
from api.models import User
from app.models import Customer,Product,Cart,OrderPlaced
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields="__all__"
        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't Match")
        else:
            user.set_password(password)
            user.save()
            return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']
    
    def validate(self,attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID: ',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token: ',token)
            link="http://localhost:3000/api/user/reset/"+uid+"/"+token
            print('password reset link: ',link)

            # send email
            body="Click following link reset your your password"+link
            data={
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a registered user')
class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']

    def validate(self,attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            else:
                id=smart_str(urlsafe_base64_decode(uid))
                user=User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                    raise serializers.ValidationError("Token is not valid or expired")
                user.set_password(password)
                user.save()
                return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("token is not valid or expired")

# app api
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class OrderPlacedSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderPlaced
        fields='__all__'