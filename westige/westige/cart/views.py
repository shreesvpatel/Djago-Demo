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


     #============================================= cart or wishlist =======================================#
      
class CartOrWishlistAdd(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            product=request.query_params.get("product")
            print("product =====================>",product)
            Status=request.query_params.get("status")
            print("Status =====================>",Status)           
            productget=Products.objects.filter(p_id=product).first()
            
            if not productget:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid product id  ","data":{}})
            if not productget.p_quantity > 0:
               return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" product out of stock  ","data":{}})
           
            print("item called() ==========================>")
            item=CartAndWishlist.objects.filter(Q(user=user)&Q(product=productget.id)&Q(status=Status)).first()
            print("item =========================>",item)
            data=request.data.copy()
            data["user"]=user.id
            data["product"]=productget.id
            data["status"]=Status
            
            print("data =====================>",data)
            
                
            serializer=CartOrWishlistSerializer(data=data)
            print("serializer =====================>",serializer)
            
            serializer.is_valid(raise_exception=True)
            print("serializer =====================>",serializer)
            if item:     
                return Response({"status":status.HTTP_201_CREATED,"message":" cart or wishlist item added ","data":serializer.data}) 
            serializer.save()   
            return Response({"status":status.HTTP_201_CREATED,"message":" cart or wishlist item added ","data":serializer.data})
        
        except:
            raise 
        
class CartOrWishlistUpdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            user=request.user.id
            product=request.query_params.get("product")
            Status=request.query_params.get("status")
            print("product ===============>",product)
            productget= Products.objects.filter(p_id=product).first()
            print("productget -=====================>",productget)
            if not productget.p_quantity > 0:
               return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" product out of stock  ","data":{}})
            item=CartAndWishlist.objects.filter(Q(user=user)&Q(product=productget.id)&Q(status=Status)).first()
            print("item ================>",item)
            if not item:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid product detail  ","data":{}})
            serializer=CartOrWishlistUpdateSerializer(item,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_201_CREATED,"message":" cart or wishlist item updated ","data":serializer.data})
        
        except:
            raise 
        
        
class CartOrWishlistGet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        try:
            user=request.user.id
            product=request.query_params.get("product")
            Status=request.query_params.get("status")
            if product:
                items=CartAndWishlist.objects.filter(Q(user=user)&Q(product=product)&Q(status=Status))
            else:
                items=CartAndWishlist.objects.filter(Q(user=user)&Q(status=Status))
            if not items:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid product detail ","data":{}})

            serializer=CartOrWishlistGetSerializer(items,many=True)
            
            total_amount = 0           
            for item in items:
                total_amount += item.product.total_price
            item_count=items.count()
            return Response({"status":status.HTTP_201_CREATED,"message":" cart or wishlist item updated ","total_amount":total_amount,"item count":item_count,"data":serializer.data})
        
        except:
            raise 


class CartOrWishlistDelete(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        try:
            user=request.user.id
            product=request.query_params.get("product")
            Status=request.query_params.get("status")  
            item=CartAndWishlist.objects.filter(Q(user=user)&Q(product=product)&Q(status=Status)).first()
            print("item ================>",item)
            if not item:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" invalid product detail  ","data":{}})
            item.delete()     
            return Response({"status":status.HTTP_201_CREATED,"message":" cart or wishlist item deleted","data":{}})
        
        except:
            raise 