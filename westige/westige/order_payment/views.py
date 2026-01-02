from django.shortcuts import render
from .serializer import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from westige.pagination import *
from westige.utils import *
from .models import *
from westige_project import settings
import razorpay
import json
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))


     #============================================= Confirm Address =======================================#

class ConfirmAddress(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            user= UserMaster.objects.filter(email=user.email).first()
            if not user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid user ","data":{}})
            data=request.data.copy()
            data["user"]=user.id
            serializer=ConfirmAdressSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            user_adddress=OrderAddress.objects.filter(user=user.id).first()            
            if not user_adddress :
                serializer.save()         
                return Response({"status":status.HTTP_201_CREATED,"message":"address confirmed","data":serializer.data})
            return Response({"status":status.HTTP_201_CREATED,"message":"already has saved address if want to change anything then update address","data":serializer.data})
        except:
            raise 

class GetConfirmAddress(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            user= UserMaster.objects.filter(email=user.email).first()
            if not user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid user ","data":{}})

            user_adddress=OrderAddress.objects.filter(user=user.id).first()            
            if not user_adddress :   
                return Response({"status":status.HTTP_201_CREATED,"message":"user not save their address","data":{}})
            serializer = ConfirmAdressSerializer(user_adddress)
            return Response({"status":status.HTTP_201_CREATED,"message":"user address ","data":serializer.data})
        except:
            raise 
        
class UpdateAddress(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            user=request.user
            user= UserMaster.objects.filter(email=user.email).first()
            if not user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid user ","data":{}})
            user_address=OrderAddress.objects.filter(user=user.id).first()
            if not user_address:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" not have stored user adddress ","data":{}})
            serializer=UpdateAdressSerializer(user_address,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_201_CREATED,"message":"address confirmed","data":serializer.data})

        except:
            raise 
        

class DeleteConfirmAddress(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            user= UserMaster.objects.filter(email=user.email).first()
            if not user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid user ","data":{}})
            user_adddress=OrderAddress.objects.filter(user=user.id).first()            
            if not user_adddress :   
                return Response({"status":status.HTTP_201_CREATED,"message":"user not save their address","data":{}})
            user_adddress.delete()
            return Response({"status":status.HTTP_200_OK,"message":"user address delete successsfull","data":{}})
        except:
            raise 
        
     #============================================= Orders & Payment =======================================#

class CreatePaymentLinkAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentLinkSerializer(
            data=request.data,
            context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]
        address = serializer.validated_data["address"]
        payment_method = serializer.validated_data["payment_method"]
        total_amount = product.total_price * quantity

        order = Orders.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_amount=total_amount,
            address=address,
            payment_status="pending",
            order_status="pending",
            payment_method = payment_method
        )
        
        if payment_method == "online":
            
            payment_link = razorpay_client.payment_link.create({
                "amount": int(total_amount * 100),  # amount in paise
                "currency": "INR",
                "description": f"Order #{order.id}",
                "customer": {
                    "name": request.user.name,
                    "email": request.user.email,
                    
                },
                "notify": {"email": True, "sms": True},
                "callback_method": "get",
                "notes":{"product_id":product.p_id,
                    "quantity": quantity,
                    "order_id":order.id}
                
            })
            print("payment_link =====================>",payment_link)
            
            order.razorpay_payment_id = payment_link.get("id")
            order.save()
            print("order.razorpay_payment_link_id ==============>",order.razorpay_payment_id)
            print("order.id ===================>",order.id)
            return Response({
                "status": "success",
                "message": "Payment link created",
                "order_id": order.id,
                "payment_link": payment_link.get("short_url"),
                "amount": total_amount,
                "currency": "INR"
            })
            
        return Response({
                "status": "success",
                "message": "cod order created",
                "amount": total_amount,
                "payment_method":payment_method
            })

class WebHookApi(APIView):
    def post (self,request):
        payload = request.body
        signature = request.headers.get("X-Razorpay-Signature") 

        data = json.loads(payload)
       
        if data.get("event") == "payment_link.paid":
            payment_entity = data["payload"]["payment"]["entity"]

            payment_id = payment_entity["id"]
            order_id = payment_entity.get("order_id")
            amount = payment_entity["amount"] / 100
            product_id = payment_entity["notes"]["product_id"]
            paymentorder_id = payment_entity["notes"]["order_id"]
            print("webhook order id  ======================>",paymentorder_id)
            product = Products.objects.filter(p_id=product_id).first()
            # if not product:
            #     return Response({"error": "Product not found"}, status=404)

            order = Orders.objects.filter(id=paymentorder_id).first()
            if not order:
                return Response({"error": "Order not found"}, status=404)
            
            print("product.p_quantity ================>",product.p_quantity)
            product.p_quantity-= 1
            product.save()
            
            
            order.razorpay_order_id = order_id
            order.razorpay_payment_id = payment_id
            order.payment_status = "paid"        
            order.order_status = "confirmed"
            order.total_amount = amount
            order.save()

            print(" order upated in database ==================>:", order.id)
        return Response({"status": "ok"}, status=200)


class RefundApi(APIView):
    def post(self,request):
        
        serializer=RefundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order_id = serializer.validated_data.get("order_id")
        order = Orders.objects.filter(razorpay_order_id=order_id).first()
        
        if not order :
            return Response ({"status":status.HTTP_404_NOT_FOUND, "message":" order not found ","data":{}})
        
        if not order.payment_status == "paid":
            return Response ({"status":status.HTTP_404_NOT_FOUND, "message":f" {order.payment_status} payment ","data":{}})
        
        amount_in_paise = int(order.total_amount)*100
        amount= {"amount":amount_in_paise}
        refund = razorpay_client.payment.refund(order.razorpay_payment_id,amount)
        
        if refund :
            order.payment_status = "refunded"
            order.product.p_quantity += 1
            order.save()
            return Response ({"status":status.HTTP_200_OK, "message":"refund successful ","data":{}})
            
        return Response ({"status":status.HTTP_404_NOT_FOUND, "message":"refund unsuccessful ","data":{}})
    
class SellerOreder(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_classes = CustomPageNumberPagination
    def post(self,request):
        try:
            
            user=UserMaster.objects.filter(email=request.user.email ).first()
            if not user.is_seller :
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" only seller can access this api  ","data":{}})
            order=Orders.objects.filter(product__p_seller = user)
            paginator= self.pagination_classes()
            paginate_queryset= paginator.paginate_queryset(order,request)
            serializer= SellerOrderSerializer(paginate_queryset,many=True)
            
            return paginator.get_paginated_response(serializer.data)

        except:
            raise 

class OrderDateFilter(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_classes = CustomPageNumberPagination
    def post(self,request):
        try:

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            
            user=UserMaster.objects.filter(email=request.user.email ).first()
            if not user.is_seller :
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" only seller can access this api  ","data":{}})
            
            seller_order = Orders.objects.filter(product__p_seller = user)

            if not end_date:
                order = seller_order.filter(created_at__date__gte = start_date)
            elif start_date and end_date:
                order = seller_order.filter(created_at__date__range=[start_date,end_date])
            else:
                order= seller_order
            
            paginator= self.pagination_classes()
            paginate_queryset= paginator.paginate_queryset(order,request)
            serializer= SellerOrderFilterSerializer(paginate_queryset,many=True)
            
            return paginator.get_paginated_response(serializer.data)

        except:
            raise 
        
class OrderConfirmStep(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,IsAdminUser]
    def put(self,request):
        try:
            if not request.user.is_seller:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"only seller can confirm order","data":{}})
            oreder_id=request.query_params.get("oreder_id")
            orderstatus= request.query_params.get("orderstatus")
            order=Orders.objects.filter(oreder_id=oreder_id).first()
            if not order:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid oreder id ","data":{}})
            if not orderstatus in ["pending","confirm","shipping","completed"] :
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid oreder status ","data":{}})
            order.order_status=orderstatus
            order.save()
            return Response({"status":status.HTTP_201_CREATED,"message":" order status changed ","data":{"order_status":orderstatus}})

        except:
            raise 