from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from westige.utils import *
from django.db.models import Q
from decimal import Decimal
import razorpay
from westige_project import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))


class ConfirmAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model= OrderAddress
        fields = "__all__"
    
    def validate(self, attrs):
        phone=attrs.get("phone")
        user=attrs.get("user")
        if not len(phone) == 10:
            raise serializers.ValidationError("invalid phone number")
        return attrs

        
class UpdateAdressSerializer(serializers.Serializer):
    name=serializers.CharField(required=False)
    nickname= serializers.CharField(required=False)
    phone= serializers.IntegerField(required=False)
    address= serializers.CharField(required=False)
    city= serializers.CharField(required=False)
    pincode= serializers.CharField(required=False)
   
        
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name",instance.name)
        instance.nickname = validated_data.get("nickname",instance.nickname)
        instance.address = validated_data.get("address",instance.address)
        instance.city = validated_data.get("city",instance.city)
        instance.pincode = validated_data.get("pincode",instance.pincode)
        
        return instance
    

class PaymentLinkSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    payment_method = serializers.CharField(required=False)

    def validate(self, attrs):
        user = self.context["user"]
        address = OrderAddress.objects.filter(user=user).first()
        if not address:
            raise serializers.ValidationError("Address not found")

        product = Products.objects.filter(id=attrs["product_id"]).first()
        if not product:
            raise serializers.ValidationError("Product not found")
        if not product.p_quantity > 0:
            raise serializers.ValidationError("product not instock")
            

        if attrs["quantity"] > product.p_quantity:
            raise serializers.ValidationError("Not enough stock")

        attrs["address"] = address
        attrs["product"] = product
        return attrs


# ==========================================\
    #  RAZORPAY PAYMENT 
# =========================================== 
   
# class PlaceOrderSerializer(serializers.Serializer):
#     product_id = serializers.IntegerField()
#     quantity = serializers.IntegerField(min_value=1)
#     payment_method = serializers.ChoiceField(
#         choices=[("online", "Online"), ("cod", "COD")]
#     )
#     currency = serializers.ChoiceField(choices=[("INR", "INR")])

#     def validate(self, attrs):
#         user = self.context["user"]

#         address = OrderAddress.objects.filter(user=user).first()
#         if not address:
#             raise serializers.ValidationError("Address not found")
       
#         product = Products.objects.filter(id=attrs["product_id"]).first()
#         print("product ================>",product)
#         if not product:
#             raise serializers.ValidationError("Product not found")

#         if attrs["quantity"] > product.p_quantity:
#             raise serializers.ValidationError("Not enough stock")

#         attrs["address"] = address
#         attrs["product"] = product
#         print("attrs ================>",attrs)
#         return attrs

#     def create(self, validated_data):
#         user = self.context["user"]
#         prod = validated_data["product"]
#         quantity = validated_data["quantity"]
#         payment_method = validated_data["payment_method"]
#         currency = validated_data["currency"]
#         address = validated_data["address"]
        
#         product = Products.objects.filter(id=prod.id).first()
        
#         total_amount = product.total_price * quantity
#         amount_paise = int(total_amount * 100)
#         print("validated_data ================>",validated_data)
#         print("total_amount ================>",total_amount)
#         order = Orders.objects.create(
#             user=user,
#             address=address,
#             product=product,
#             quantity=quantity,
#             total_amount=total_amount
#         )
#         print("order ================>",order)
#         response = {
#             "order_id": order.id,
#             "amount": amount_paise,
#             "currency": currency
#         }

#         if payment_method == "online":
#             razorpay_order = razorpay_client.order.create({
#                 "amount": amount_paise,
#                 "currency": currency,
#                 "payment_capture": 0
#             })
#             order.razorpay_order_id = razorpay_order["id"]
#             order.save()

#             response.update({
#                 "razorpay_order_id": razorpay_order["id"],
#                 "razorpay_key": settings.RAZORPAY_TEST_KEY_ID
#             })
#         else:
#             order.payment_status = "cod"
#             order.order_status = "confirmed"
#             order.save()
#         print("response ================>",response)
#         return response

# class VerifyPaymentSerializer(serializers.Serializer):
#     razorpay_order_id = serializers.CharField()
#     razorpay_payment_id = serializers.CharField()
#     razorpay_signature = serializers.CharField()

#     def validate(self, attrs):
#         user = self.context["user"]
#         print("user =======================>",user)
#         order = Orders.objects.filter(
#             razorpay_order_id=attrs["razorpay_order_id"],
#             user=user
#         ).first()
#         print("order =======================>",order)

#         if not order:
#             raise serializers.ValidationError("Order not found")

#         attrs["order"] = order
#         return attrs

#     def create(self, validated_data):
#         order = validated_data["order"]

#         try:
#             razorpay_client.utility.verify_payment_signature({
#                 "razorpay_order_id": validated_data["razorpay_order_id"],
#                 "razorpay_payment_id": validated_data["razorpay_payment_id"],
#                 "razorpay_signature": validated_data["razorpay_signature"],
#             })
#         except SignatureVerificationError:
#             order.payment_status = "failed"
#             order.save()
#             raise serializers.ValidationError("Payment verification failed")

#         order.payment_status = "paid"
#         order.order_status = "confirmed"
#         order.razorpay_payment_id = validated_data["razorpay_payment_id"]
#         order.razorpay_signature = validated_data["razorpay_signature"]
#         order.save()

#         return order

class OrderConfirmStepSerializer(serializers.Serializer):
    orderid = serializers.CharField()
    
    def update(self, instance, validated_data):
        instance.order_status = validated_data.get("order")
        return instance
    




class GetallSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMaster
        fields = ["u_id","name","email","password","is_staff"]
        
class SellerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"

class SellerOrderFilterSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False) 
    class Meta:
        model = Orders
        fields = "__all__"
    

class RefundSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    amount = serializers.IntegerField(required=False)  # paise (optional for full refund)

# class PlaceOrderSerializer(serializers.Serializer):
    
#     payment_method = serializers.ChoiceField(
#         choices=[("online", "Online"), ("cod", "COD")]
#     )
#     currency = serializers.ChoiceField(choices=[("INR", "INR")])

#     def validate(self, attrs):
#         user = self.context["user"]

#         address = OrderAddress.objects.filter(user=user).first()
#         if not address:
#             raise serializers.ValidationError("Address not found")

#         cartitem = CartAndWishlist.objects.filter(user=user, status="cart")
#         if not cartitem.exists():
#             raise serializers.ValidationError("Cart is empty")

#         attrs["address"] = address
#         attrs["cartitem"] = cartitem
#         return attrs

#     def create(self, validated_data):
#         user = self.context["user"]
#         address = validated_data["address"]
#         cartitem = validated_data["cartitem"]
#         payment_method = validated_data["payment_method"]
#         currency = validated_data["currency"]
#         print(" user========>",user)
#         print("address ========>",address)
#         print("cartitem ========>",cartitem)
#         print("payment_method ========>",payment_method)
#         print("currency ========>",currency)
#         order = Orders.objects.create(
#             user=user,
#             address=address,
#             payment_status="pending",
#             order_status="pending"
#         )
#         print("order ===============>",order)
#         total_amount = Decimal("0.00")

#         for item in cartitem:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.total_price
#             )
#             total_amount += item.product.total_price * item.quantity

#         amount = int(total_amount * 100)
        
#         print("total_amount ===============>",total_amount)
#         response_data = {
#             "order_id": order.id,
#             "amount": amount,
#             "currency": currency,
#         }
#         print("response_data ===============>",response_data)
        
#         if payment_method == "online":
#             razorpay_order = razorpay_client.order.create({
#                 "amount": amount,
#                 "currency": currency,
#                 "payment_capture": 0
#             })

#             order.razorpay_order_id = razorpay_order["id"]

#             response_data.update({
#                 "razorpay_order_id": razorpay_order["id"],
#                 "razorpay_key":settings.RAZORPAY_TEST_KEY_ID  # YOUR KEY ID
#             })
            
#             print("response_data ===============>",response_data)
        
#         else:  # COD
#             order.payment_status = "cod"
#             order.order_status = "confirmed"
#         print("order ===============>",order)
#         order.total_amount = total_amount
#         order.save()
#         cartitem.delete()
#         print("response_data ===============>",response_data)
#         return response_data


# class VerifyPaymentSerializer(serializers.Serializer):
#     razorpay_order_id = serializers.CharField()
#     razorpay_payment_id = serializers.CharField()
#     razorpay_signature = serializers.CharField()

#     def validate(self, attrs):
#         user = self.context["user"]
#         print("user =======================>",user)
#         order = Orders.objects.filter(
#             razorpay_order_id=attrs["razorpay_order_id"],
#             user=user
#         ).first()
#         print("order =======================>",order)

#         if not order:
#             raise serializers.ValidationError("Order not found")

#         attrs["order"] = order
#         return attrs

#     def create(self, validated_data):
#         order = validated_data["order"]

#         try:
#             razorpay_client.utility.verify_payment_signature({
#                 "razorpay_order_id": validated_data["razorpay_order_id"],
#                 "razorpay_payment_id": validated_data["razorpay_payment_id"],
#                 "razorpay_signature": validated_data["razorpay_signature"],
#             })
#         except SignatureVerificationError:
#             order.payment_status = "failed"
#             order.save()
#             raise serializers.ValidationError("Payment verification failed")

#         order.payment_status = "paid"
#         order.order_status = "confirmed"
#         order.razorpay_payment_id = validated_data["razorpay_payment_id"]
#         order.razorpay_signature = validated_data["razorpay_signature"]
#         order.save()

#         return order