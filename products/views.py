from django.shortcuts import render,redirect
from rest_framework.response import Response
from products.models import Products,Reviews,Carts,OrderModel
from products.serializers import ReviewSerializer,ProductSerializer,CartSerializer,UserSerializer,OrderModelSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import authentication,permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class ProductView(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class = ProductSerializer
   
    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = Products.objects.filter(category=category)
        else:
            queryset = Products.objects.all()
        return queryset


    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kw):
        user=request.user 
        product=self.get_object()
        serializer=ReviewSerializer(data=request.data,context={"user":user,"product":product}) 
        if serializer.is_valid():
            serializer.save() 
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"],detail=True)
    def get_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        product=Products.objects.get(id=id)
        reviews=product.reviews_set.all()
        serializer=ReviewSerializer(reviews,many=True)
        return Response(data=serializer.data) 

    @action(methods=["POST"],detail=True)
    def addto_cart(self,request,*args,**kwargs):
        prodkt=self.get_object()
        usr=request.user
        serializer=CartSerializer(data=request.data,context={"product":prodkt,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
  
    @action(methods=["POST"],detail=True)
    def addto_order(self,request,*args,**kwargs):
        prodkt=self.get_object()
        usr=request.user
        serializer=OrderModelSerializer(data=request.data,context={"product":prodkt,"user":usr})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    @action(methods=["get"],detail=False)
    def categories(self,request,*args,**kw):
        categories=Products.objects.values_list("category",flat=True).distinct() 
        return Response(data=categories) 
    
    
class Cartsview(ModelViewSet):
    serializer_class=CartSerializer
    queryset=Carts.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

    @action(methods=["get"],detail=False)
    def get_usercartcount(self,request,*args,**kw):
        cartcount=Carts.objects.filter(user=self.request.user).count()
        return Response(data=cartcount)
    
    @action(methods=["get"],detail=False)
    def pricecount(self,request,*args,**kw):
        cart_items = Carts.objects.filter(user=request.user, status='in-cart')
        prices = [item.product.price for item in cart_items]
        total=sum(prices)
        return Response(data=total)
   
class OrderModelView(ModelViewSet):
    serializer_class=OrderModelSerializer
    queryset=OrderModel.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
    
