from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(UserMaster)
class UserMasterAdmin(admin.ModelAdmin):
    list_display=["id","name","email","u_id","address","is_seller"]
    
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display=["id","p_id","p_name","p_description","p_seller","p_quantity","created_at"]
    
@admin.register(CartAndWishlist)
class CartAndWishlistAdmin(admin.ModelAdmin):
    list_display=["user","product","quantity","status"]
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["id","c_name","c_description"]
    
@admin.register(OrderAddress)
class OrederAddressAdmin(admin.ModelAdmin):
    list_display=["name","nickname","phone","address","city","pincode"]
    
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display=["order","product__p_name","quantity","price"]
    
@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display=["user","address","payment_status","razorpay_order_id","razorpay_payment_id","product","quantity","total_amount","created_at"]
    
# @admin.register(Review)
# class ReviewAdmin(admin.ModelAdmin):
#     list_display=["user","product","message","Rate"]
    
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display=["payment_id","order","amount","payment_status"]