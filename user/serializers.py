from rest_framework import serializers
from .models import Product, User, Seller

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('UserId', 'UserName', 'mobileNo')

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('SellerName','SellerEmail', 'mobileNo', 'password')

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom Token Obtain Pair Serializer that adds custom claims to the access and refresh tokens.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['role'] = user.role
        return token


class ProductSerializer(serializers.ModelSerializer):

    def __str__(self):
        return self.name
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'image']

