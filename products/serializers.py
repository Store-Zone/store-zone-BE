from rest_framework import serializers
from products.models import Products,Reviews,Carts,OrderModel
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True) 
    class Meta:
        model=Products
        fields="__all__"

class ReviewSerializer(serializers.ModelSerializer):
    create_date=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    product=serializers.CharField(read_only=True)
    class Meta:
        model=Reviews
        fields="__all__"        
    def create(self,validated_data):
        usr=self.context.get("user")
        prodkt=self.context.get("product")
        return Reviews.objects.create(**validated_data,user=usr,product=prodkt)

class CartSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    product=ProductSerializer(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)
    
    class Meta:
        model=Carts
        fields=["id","product","user","status","created_date"]  
    def create(self,validated_data):
        usr=self.context.get("user")
        prodkt=self.context.get("product")
        return Carts.objects.create(user=usr,product=prodkt,**validated_data)   
   
class OrderModelSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    product=ProductSerializer(read_only=True)
    user=serializers.CharField(read_only=True)
    order_date=serializers.CharField(read_only=True)
    class Meta:
        model=OrderModel
        fields="__all__"
    def create(self,validated_data):
        usr=self.context.get("user")
        prodkt=self.context.get("product")
        return OrderModel.objects.create(user=usr,product=prodkt,**validated_data)