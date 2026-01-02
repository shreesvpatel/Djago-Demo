from django.contrib import admin
from .models import Payment
# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['razorpay_order_id', "razorpay_payment_id","razorpay_signature","amount","status","created_at"]