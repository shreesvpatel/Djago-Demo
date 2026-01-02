from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from decimal import Decimal
import uuid 
from westige.models import *

# class Category(models.Model):
#     c_name = models.CharField(max_length=250)
#     c_description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.c_name

# class Products(models.Model):
#     p_id = models.CharField(max_length=20, unique=True, blank=True)
#     p_name = models.CharField(max_length=250)
#     p_description = models.TextField(blank=True, null=True)
#     p_image = models.ImageField(upload_to="product/",null=True,blank=True)
#     mrp_price = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(Decimal("0.00"))])
#     discount = models.DecimalField(max_digits=5,decimal_places=2,validators=[MinValueValidator(Decimal("0.00")),MaxValueValidator(Decimal("100.00"))],default=0)    
#     total_price = models.DecimalField(max_digits=10,decimal_places=2,editable=False)
#     p_quantity = models.PositiveIntegerField(default=1)
#     p_category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name="products")
#     p_seller = models.ForeignKey(UserMaster,on_delete=models.CASCADE,related_name="seller_user")
#     created_at = models.DateTimeField(auto_now_add=True,null=False)
    
#     def save(self, *args, **kwargs):
#         if not self.p_id:
#             self.p_id = f"{self.p_name[:3].upper()}{uuid.uuid4().hex[:6]}"

#         discount_amount =int(self.mrp_price) *(int(self.discount)/100)
#         self.total_price = int(self.mrp_price) - discount_amount

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.p_id

# class Review(models.Model):
#     user = models.ForeignKey(UserMaster,on_delete=models.CASCADE,related_name="review_user")
#     product = models.ForeignKey(Products,on_delete=models.CASCADE)
#     message = models.TextField(max_length=250)
#     Rate = models.PositiveIntegerField()
    
#     def __str__(self) :
#         return self.message