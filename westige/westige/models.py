from typing import Iterable
from django.db import models
from .managers import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import random
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
import datetime
import uuid 

class UserMaster(AbstractBaseUser,PermissionsMixin):
    name= models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100,null=False)
    u_id=models.CharField(max_length=250)
    address= models.CharField(max_length=250)
    is_seller=models.BooleanField(default=False)
    otp=models.CharField(max_length=100,null=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    
    USERNAME_FIELD= "email"
    REQUIRED_FIELD=["password"]
    objects=CustomUserManager()
    def __str__(self):
        return self.email
    
    
class Category(models.Model):
    c_name = models.CharField(max_length=250)
    c_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.c_name

class Products(models.Model):
    p_id = models.CharField(max_length=20, unique=True, blank=True)
    p_name = models.CharField(max_length=250)
    p_description = models.TextField(blank=True, null=True)
    p_image = models.ImageField(upload_to="product/",null=True,blank=True)
    mrp_price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal("0.00"))])
    discount = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(Decimal("0.00")),MaxValueValidator(Decimal("100.00"))],default=0)    
    total_price = models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    p_quantity = models.PositiveIntegerField(default=1)
    p_category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="products")
    p_seller = models.ForeignKey(UserMaster,on_delete=models.CASCADE,related_name="seller_products")
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    
    def save(self, *args, **kwargs):
        if not self.p_id:
            self.p_id = f"{self.p_name[:3].upper()}{uuid.uuid4().hex[:6]}"

        discount_amount =int(self.mrp_price) *(int(self.discount)/100)
        self.total_price = int(self.mrp_price) - discount_amount

        super().save(*args, **kwargs)

    def __str__(self):
        return self.p_id

    
class CartAndWishlist(models.Model):
    STATUS_CHOICES = (
        ("cart", "Cart"),
        ("wishlist", "Wishlist"),
    )

    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("user", "product", "status")

    def __str__(self):
        return f"{self.user.email} - {self.product.p_name}"

 

class OrderAddress(models.Model):
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.address
    

# class Orders(models.Model):
#     ORDER_STATUS = (
#         ("pending", "Pending"),
#         ("confirmed", "Confirmed"),
#         ("shipped", "Shipped"),
#         ("delivered", "Delivered"),
#         ("cancelled", "Cancelled"),
#     )

#     PAYMENT_STATUS = (
#         ("pending", "Pending"),
#         ("paid", "Paid"),
#         ("failed", "Failed"),
#         ("cod", "Cash On Delivery"),
#     )

#     order_id = models.CharField(max_length=20, unique=True, blank=True)
#     user = models.ForeignKey(UserMaster, on_delete=models.CASCADE,null=True,blank=True)
#     address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE,null=True,blank=True)
#     # product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     # quantity = models.PositiveIntegerField(default=1)
#     # total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="pending")
#     order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")   
#     razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
#     razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
#     razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#           return f"Order #{self.id}"   
 
# class OrderItem(models.Model):
#     order = models.ForeignKey(Orders,related_name="items",on_delete=models.CASCADE)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def save(self, *args, **kwargs):
#         if not self.price:
#             self.price = self.product.total_price
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.product.p_name
    
# class Payment(models.Model):
#     PAYMENT_METHOD_CHOICES = (
#         ('qr', 'QR_CODE'),
#         ('netbanking','Net_Banking'),
#         ('cashondelivery', 'Cash_On_Delivery'),
#     )
    
#     PAYMENT_STATUS_CHOICES = (
#         ('pending', 'pending'),
#         ('processing','Processing'),
#         ('confirmed', 'confirmed'),
#     )
#     order= models.ForeignKey(Orders,on_delete=models.CASCADE,null=True)
#     payment_id = models.CharField(max_length=250,unique=True,null=True)
#     payment_status = models.CharField(max_length=250,choices=PAYMENT_STATUS_CHOICES)
#     payment_method = models.CharField(max_length=250,choices=PAYMENT_METHOD_CHOICES)
#     amount = models.PositiveIntegerField(max_length=250)
    
    
#     def __str__(self) :
#         return self.payment_id
    
#     def save(self,*args,**extra_fields):
#         if not self.payment_id:
#             uid = uuid.uuid4()
#             id =str(uid).replace("-","")[:10]
#             self.payment_id=id
            
#             if self.payment_status == "confirmed":
#                 order=Orders.objects.filter(id=self.order.id).first()
#                 order.payment_status="confirmed"
#                 order.save()
#                 return super().save()
#             return super().save()
#         if self.payment_status == "confirmed":
#             order=Orders.objects.filter(id=self.order.id).first()
#             order.payment_status="confirmed"
#             order.save()
#             return super().save()
        
#         return super().save()

class Review(models.Model):
    user = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    message = models.TextField(max_length=250)
    Rate = models.PositiveIntegerField()
    
    def __str__(self) :
        return self.message

# class Products(models.Model):
#     p_id = models.CharField(null=True,blank=True,unique=True)
#     p_name = models.CharField(max_length=250,null=True)
#     p_description = models.CharField(max_length=250,null=True)
#     mrp_price = models.IntegerField(null=True)
#     discount= models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(Decimal('0.00')),MaxValueValidator(Decimal('99.99'))],default=0.00)   
#     total_price = models.IntegerField(null=True)
#     p_quantity = models.IntegerField(null=True)
#     p_category = models.ForeignKey(Category,on_delete=models.CASCADE)
#     p_seller = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.p_id
    
#     def save(self,*args,**kwargs):
#         if not self.p_id:
#             id_prefix=self.p_name[:3].upper()
#             
#             id_number = random.randint(000,999)
#             id=f"{id_prefix}{id_number}"
#             self.p_id=id 
#             
#             if not self.discount:              
#                 self.total_price = self.mrp_price
#                 return super().save()
#             discount_price =self.mrp_price *(self.discount/100)
#             print("discount_price ===============>",discount_price)
#             total_price= self.mrp_price - discount_price
#             print("total_price ================>",total_price)
#             self.total_price = total_price
#             return super().save()
        
#         if not self.discount:   
#             self.total_price = self.mrp_price
#             return super().save()
    
#         discount_price =self.mrp_price *(int(self.discount)/100)
#         total_price= self.mrp_price - discount_price
        
#         self.total_price = total_price
#         return super().save()
   
# class CartAndWishlist(models.Model):
#     user = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
#     product = models.ForeignKey(Products,on_delete=models.CASCADE)
#     quantity= models.IntegerField(default=1)
#     status = models.CharField(max_length=250)

# class OrederAddress(models.Model):
#     user = models.ForeignKey(UserMaster,on_delete=models.CASCADE,null=True)
#     name =  models.CharField(max_length=250)
#     phone = models.CharField(max_length=250,unique=True)
#     nickname =  models.CharField(max_length=250,null=True)
#     address =  models.CharField(max_length=250)
#     city =  models.CharField(max_length=250)
#     pincode =  models.CharField(max_length=250)
    
#     def __str__(self):
#         return self.address   
    
# class Orders(models.Model):
#     oreder_id = models.CharField(max_length=250,null=True,unique=True)
#     orderitem = models.ForeignKey(OrderItem,on_delete=models.CASCADE)
#     user = models.ForeignKey(UserMaster,on_delete=models.CASCADE)
#     orderaddress = models.ForeignKey(OrderAddress,on_delete=models.CASCADE)
#     payment_method = models.CharField(max_length=250)
#     payment_status = models.CharField(max_length=250,default="pending")
#     order_status = models.CharField(max_length=250,default="pending")
#     order_date = models.DateTimeField(auto_now_add=True,null=True)
#     order_deliver_date = models.DateTimeField(null=True,blank=True)
    
#     def __str__(self) :
#         return self.oreder_id
    
#     def save(self,*args,**kwargs):
#         print("save() called ==========================")
#         if not self.oreder_id:
#             print(" have order status called ==========================")
#             id = random.randint(000000,999999)
#             self.oreder_id=id
#             return super().save()
#         print("not have order id called ==========================")
#         if self.order_status  == "completed":
#             self.order_deliver_date = datetime.datetime.now()

        # return super().save()
           
# class OrderItem(models.Model):
#     product = models.ForeignKey(Products,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     total_amount= models.PositiveIntegerField(null=True)
    
#     def __str__(self):
#         return self.product.p_id
    
#     def save(self,*args,**extra_fields):
#         self.total_amount
#         amount=self.product.total_price * self.quantity
#         self.total_amount=amount
#         return super().save()

class Orders(models.Model):
    ORDER_STATUS = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("cod", "Cash On Delivery"),
        ("online","Online")
    )

    # order_id = models.CharField(max_length=20, unique=True, blank=True,null=True)
    user = models.ForeignKey(UserMaster, on_delete=models.CASCADE,null=True,blank=True)
    address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    payment_status = models.CharField(max_length=20, default="pending")
    order_status = models.CharField(max_length=20, default="pending")   
    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
    payment_method = models.CharField(max_length=250,choices=PAYMENT_METHOD_CHOICES,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

  
 