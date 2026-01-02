from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from westige_project import settings
import random

def get_token_for_user(user):
    try:
        token=Token.objects.get(user=user)
    except:
        token=Token.objects.create(user=user)
        
    return token.key

def send_otp_mail(user):
    
    otp =random.randint(0000,9999)
    email=user.email
    send_mail(
        subject="ONE - TIME PASSWORD",
        message="we received request for forgot password",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user])
    
    user.otp=otp
    user.save()
    
    return user  


def send_product_placed_mail(product):
    seller=product.p_seller
    print("send_product_placed_mail() called ==========================>")
    send_mail(
        subject=" PRODUCT PLACED ",
        message=f"order placed for {product.p_name} with price :{product.total_price} ",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[seller])
    
    return product


def send_order_placed_mail(user):
    user=user.email
    print("send_product_placed_mail() called ==========================>")
    send_mail(
        subject=" PRODUCT PLACED ",
        message=f" {user} your order has been placed ",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user])
    
    return user