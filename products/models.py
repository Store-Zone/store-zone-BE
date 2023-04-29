from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator


class Products(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='productimages',blank=True)
    price=models.PositiveIntegerField()
    category=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    qty=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE) 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=150)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    create_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

class Carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("in-cart","in-cart"),
        ("cancelled","cancelled"),
        ("order-placed","order-placed")
    )
    status=models.CharField(max_length=120,choices=options,default="in-cart")
    qty=models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product 
    
class OrderModel(models.Model):
    name=models.CharField(max_length=200)
    mobile=models.PositiveIntegerField()
    address=models.CharField(max_length=500)
    landmark=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pin=models.PositiveIntegerField()
    payment=models.CharField(max_length=500)
    order_date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)  

    def __str__(self):
        return self.address 
