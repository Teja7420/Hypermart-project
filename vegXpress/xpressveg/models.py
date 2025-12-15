from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class UserRoles(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    CUSTOMER = 'customer', 'Customer'

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=150,unique=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    role = models.CharField(max_length=15,choices=UserRoles.choices,default=UserRoles.CUSTOMER)


    USERNAME_FIELD = "email"         
    REQUIRED_FIELDS = ['username']
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products",default=None)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_image = models.ImageField(upload_to="product_image/", null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product"
  
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="order",default=None)
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name = "buyer",default=None)
 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,default=None, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=None)
    quantity = models.PositiveIntegerField(default=1)   
    total_amount = models.DecimalField(max_digits= 10,decimal_places=2,default=0.0
            )