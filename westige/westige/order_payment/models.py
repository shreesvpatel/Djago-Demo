from django.db import models
from westige.models import UserMaster,OrderAddress,Orders
from westige.product.models import Products


# class OrderAddress(models.Model):
#     user = models.ForeignKey(UserMaster, on_delete=models.CASCADE,related_name="orderaddress_user")
#     name = models.CharField(max_length=250)
#     phone = models.CharField(max_length=15)
#     nickname = models.CharField(max_length=100, blank=True, null=True)
#     address = models.TextField()
#     city = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)

#     def __str__(self):
#         return self.address
    
    

# class Orders(models.Model):
#     ORDER_STATUS = (
#         ("pending", "Pending"),
#         ("confirmed", "Confirmed"),
#         ("shipped", "Shipped"),
#         ("delivered", "Delivered"),
#         ("cancelled", "Cancelled"),
#     )

#     PAYMENT_METHOD_CHOICES = (
#         ("cod", "Cash On Delivery"),
#         ("online","Online")
#     )

#     # order_id = models.CharField(max_length=20, unique=True, blank=True,null=True)
#     user = models.ForeignKey(UserMaster, on_delete=models.CASCADE,null=True,blank=True,related_name="order_user")
#     address = models.ForeignKey(OrderAddress, on_delete=models.CASCADE,null=True,blank=True)
#     product = models.ForeignKey(Products, on_delete=models.CASCADE,null=True,blank=True)
#     quantity = models.PositiveIntegerField(default=1)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
#     payment_status = models.CharField(max_length=20, default="pending")
#     order_status = models.CharField(max_length=20, default="pending")   
#     razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
#     razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)
#     razorpay_signature = models.CharField(max_length=500, blank=True, null=True)
#     payment_method = models.CharField(max_length=250,choices=PAYMENT_METHOD_CHOICES,null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    