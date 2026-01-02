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


     #============================================= product =======================================#
       
        
class ProductAdd(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def post(self,request):
        try:
            user=request.user
            if not user.is_seller:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"only seller can add product","data":{}})
            data=request.data.copy()
            data["p_seller"]=user.id
            serializer=ProductAdd1Serializer(data=data,context={"user":user})
            serializer.is_valid(raise_exception=True)
            product=serializer.save()
            return Response({"status":status.HTTP_201_CREATED,"message":" product added","data":serializer.data})
        except:
            raise 
 
class ProductGet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        try:
            user=request.user
            products=Products.objects.filter(p_seller=user.id)
            p_id= request.query_params.get("p_id")
            p_name= request.query_params.get("p_name")
            if p_id:
                queryset = products.filter(p_id=p_id)          
            elif p_name:
                queryset= products.filter(p_name=p_name)
            else: 
                queryset=products.all()
            
            serializer=ProductGEtSerializer(queryset,many=True)
            return Response({"status":status.HTTP_200_OK,"message":" product data get ","data":serializer.data})
        except:
            raise 
        
class ProductUpdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            if not request.user.is_seller:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"only seller can update product","data":{}})
            p_id=request.query_params.get("p_id")
            product=Products.objects.filter(p_seller=request.user.id).filter(p_id=p_id).first()
      
            if not product:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"not have any product with given product id ","data":{}})
            
            serializer=ProductUpdateSerializer(product,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_200_OK,"message":" product updated","data":serializer.data})
        except:
            raise 

class ProductDelete(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def delete(self,request):
        try:
            if not request.user.is_seller:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"only seller can delete product","data":{}})
            p_id=request.query_params.get("p_id")
            product=Products.objects.filter(p_seller=request.user.id).filter(p_id=p_id).first()
            if not product:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"not have any product with given product id ","data":{}})
            product.delete()
            return Response({"status":status.HTTP_200_OK,"message":" product deleted","data":{}})
        except:
            raise 
   
     #============================================= category =======================================#
   
        
class CategoryAdd(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def post(self,request):
        try:
            if not request.user.is_seller:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"only seller can add category","data":{}})
            
            serializer=CategoryAddSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product=serializer.save()
            return Response({"status":status.HTTP_201_CREATED,"message":" category added ","data":{}})
        except:
            raise 
        
class CategoryGet(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    
    def get(self,request):
        try:
            user=request.user
            categories=Category.objects.all()
            id= request.query_params.get("id")
            c_name= request.query_params.get("c_name")
            if id:
                queryset = categories.filter(id=id)          
            elif c_name:
                queryset= categories.filter(c_name__contains=c_name)
            else: 
                queryset=categories.all()
            
            serializer=CategoryAddSerializer(queryset,many=True)
            return Response({"status":status.HTTP_200_OK,"message":" product data get ","data":serializer.data})
        except:
            raise 
        
class CategoryUpdate(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def put(self,request):
        try:
            
            id= request.query_params.get("id")
            if not id :
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"id is required","data":{}})
            category = Category.objects.filter(id=id).first()     
            serializer=CategoryAddSerializer(category,data=request.data)
            serializer.is_valid(raise_exception=True)
            product=serializer.save()
            return Response({"status":status.HTTP_201_CREATED,"message":" category updated ","data":serializer.data})
        except:
            raise 
        
class CategoryDelete(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    def delete(self,request):
        try:
        
            id=request.query_params.get("id")
            category=Category.objects.filter(id=id).first()
            if not category:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"not have any category with given id ","data":{}})
            category.delete()
            return Response({"status":status.HTTP_200_OK,"message":" product deleted","data":{}})
        except:
            raise
        
     #============================================= Product Filter By User =======================================#

class ProductFilterUser(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_classes = CustomPageNumberPagination
    def post(self,request):
        try:
            user=request.user.id
            product_name=request.query_params.get("product_name")
            product_category=request.query_params.get("product_category")  
            product_price = request.query_params.get("product_price")  
            print(" product_name==============================>",product_name)
            print("product_category ==============================>",product_category)
            print("product_price ==============================>",product_price)
            
            if product_name:
                product = Products.objects.filter(p_name__contains = product_name)
            # elif  product_price :
            #     product = Products.objects.filter(p_price= product_category)
            elif  product_category :
                product = Products.objects.filter(p_category__c_name__contains = product_category)
            else:
                product = Products.objects.all()
            print("product ==============================>",product)
            paginator = self.pagination_classes()
            paginated_queryset = paginator.paginate_queryset(product,request)
            serializer = ProductAdd1Serializer(paginated_queryset,many=True)
            
                   
            return paginator.get_paginated_response(serializer.data)
        
        except:
            raise 