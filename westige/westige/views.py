from django.shortcuts import render
from .serializer import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .pagination import *
from .utils import *
from .models import *
from westige_project import settings
import razorpay
import json
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_TEST_KEY_ID, settings.RAZORPAY_TEST_KEY_SECRET))
     #============================================= user =======================================#


class Registration(APIView):
    def post(self,request):
        try:
            print(request.data)
            email=request.data.get("email")
            seller=request.query_params.get("is_seller")
            user=UserMaster.objects.filter(email=email).first()
            if user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"user already registerd","data":{}})
            serializer=RegisterSerializer(data=request.data,context={"is_seller":seller})
            serializer.is_valid(raise_exception=True)
            user=serializer.save()
            token=get_token_for_user(user)
            print(token)
            return Response({"status":status.HTTP_201_CREATED,"message":"user registered ","toekn":token,"data":{}})
        except:
            raise
        
class Login(APIView):
    def post(self,request):
        try:
            serializer=LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email=serializer.validated_data.get("email")
            user=UserMaster.objects.filter(email=email).first()
            token=get_token_for_user(user)
            print(token)
            return Response({"status":status.HTTP_200_OK,"message":" user login successful","token":token,"data":{}})
        except:
            raise 
        
class Profile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    pagination_classes = [CustomPageNumberPagination]
    def get(self,request):
        try:
            email=request.user.email
            if email:
              user=UserMaster.objects.filter(email=email).first()
              if not user:
                return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"Invalid email","data":{}})
              serializer=Profileserializer(user)
              return Response({"status":status.HTTP_200_OK,"message":"single user data","data":serializer.data})
            user=UserMaster.objects.all()
            serializer=Profileserializer(user,many=True)

            paginator = self.pagination_classes()
            data = paginator.paginate_queryset(user, request)
            serializer = Profileserializer(data, many=True)
            return paginator.get_paginated_response(serializer.data)
          
        except :
            raise
        
class EditProfile(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def put(self,request):
        try:
            email=request.user.email
            user=UserMaster.objects.filter(email=email).first()
            serializer=EditProfileserializer(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_200_OK,"message":" user login successful","data":serializer.data})
        except:
            raise 
        
class ChangePassword(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            email=request.user.email
            user=UserMaster.objects.filter(email=email).first()
            print("user.password ===================>",user.password)
            serializer=ChangePasswordserializer(data=request.data,context={"user":user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_200_OK,"message":"change password successful","data":serializer.data})
        except:
            raise 
        
class ForgotPassword(APIView):
    def post(self,request):
        try:
            email=request.query_params.get("email")
            print("email ==========================>",email)
            serializer=ForgotPasswordSerializer(data={"email":email})
            serializer.is_valid(raise_exception=True)
            # user=UserMaster.objects.filter(email=request.data.get("email")).first()
            return Response({"status":status.HTTP_200_OK,"message":"An otp has been send to your email ","data":{}})  
            
        except :
            raise
  
class OtpVerify(APIView):
    def post(self,request):
        try:
            email=request.query_params.get("email")
            data=request.data.copy()
            data["email"]=email
            print("data =======================>",data)
            serializer=OtpVerifySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response({"status":status.HTTP_200_OK,"message":"otp verified","data":{}})  
            
        except :
            raise  

class PasswordReset(APIView):
    def post(self,request):
        try:
            email=request.query_params.get("email")
            data=request.data.copy()
            data["email"]=email
            print("data ==============================>",data)
            serializer=PasswordResetSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status":status.HTTP_200_OK,"message":"reset password successfully ","data":{}})  
            
        except :
            raise
        
class LogOut(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            user=request.user
            token = Token.objects.get(user=user.id).delete()
            return Response({"status":status.HTTP_200_OK,"message":" Log Out Successsfully ","data":{}})  
        
        except Token.DoesNotExist:
            return Response({"status":status.HTTP_200_OK,"message":" Invalid TOken","data":{}})  
        

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
  
    #============================================= Admin Side Api =======================================#

   
class Get_all_Seller(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAdminUser]
    pagination_classes = CustomPageNumberPagination
    def post(self,request):
        try:
            
            seller= UserMaster.objects.filter(is_seller=True)
            print("seller ====================>",seller)
            # serializer=GetallSellerSerializer(seller,many=True)
            paginator = self.pagination_classes()
            data = paginator.paginate_queryset(seller, request)
            serializer = Profileserializer(data, many=True)
            return paginator.get_paginated_response(serializer.data)         

        except:
            raise
        
    #============================================= Index Page Api =======================================#
   
              
def Index_call(request):
    print("index_call () function call  ===================#")
    products= Products.objects.all()
    payment_methods=["cod","online"]
    return render(request, 'index.html', {"products": products,"payment_methods":payment_methods})
   
        

# ==========================================/
    #  RAZORPAY PAYMENT 
# =========================================== 
# class PlaceOrder(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = UserMaster.objects.filter(email=request.user.email).first()
#         if not user:
#             return Response(
#                 {"message": "Invalid user"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = PlaceOrderSerializer(
#             data=request.data,
#             context={"user": user}
#         )
#         serializer.is_valid(raise_exception=True)
#         print("serializer ======================>",serializer)

#         response_data = serializer.save()
#         print("serializer.response_data ======================>",response_data)
#         print("response_data.razorpay_key ======================>",response_data["razorpay_key"])
#         return Response({
#             "status": status.HTTP_201_CREATED,
#             "message": "Order placed successfully",
#             "data": response_data
#         })


# class VerifyRazorpayPayment(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = VerifyPaymentSerializer(
#             data=request.data,
#             context={"user": request.user}
#         )
#         serializer.is_valid(raise_exception=True)
#         order=serializer.save()
#         response_data={
#             "razorpay_key":settings.RAZORPAY_TEST_KEY_ID,
#             "amount": order
#         }
#         return Response({"message": "Payment verified"}, status=200)



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
        
# class ReviewAdd(APIView):
#     authentication_classes=[TokenAuthentication]
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         try:
#             user= request.user
#             if UserMaster.objects.filter(Q(email=user.email)& Q(is_seller=True)).first():
#                 return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" seller can not give review of product ","data":{}})
#             p_id=request.query_params.get("p_id")
#             print("p_id ================>",p_id)
#             product= Products.objects.filter(p_id=p_id).first()
#             print("product ================>",product)
#             if not product:
#                 return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"invalid product ","data":{}})
#             data=request.data.copy()
#             data["product"]=product.id
#             data["user"]=user.id
#             serializer = ReviewAddserializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             print("serializer ================>",serializer)
#             serializer.save()
#             return Response({"status":status.HTTP_201_CREATED,"message":"review added","data":serializer.data})

#         except:
#             raise
        
# class GenerateQrCode(APIView): qr code through upiid and account manage 
# class Netbanking(APIView): upiid and account related data manage
# class Cash_on_delivery(APIView): payment status pending 
    
    
# class PaymentApi(APIView):
#     def post(self,request):
#         try:
#             order=request.query_params.get("order")
#             order= Orders.objects.filter(oreder_id=order).first()
#             if not order:
#                 return Response({"status":status.HTTP_400_BAD_REQUEST,"message":"invalid order id  ","data":{}})
#             payment= Payment.objects.filter(order=order).first()
#             if payment :
#                 return Response({"status":status.HTTP_400_BAD_REQUEST,"message":" payment already created for given order id  ","data":{}})
#             data= request.data.copy()
#             data["order"]=order.id
#             serializer = Paymentserializer(data=data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response({"status":status.HTTP_201_CREATED,"message":"payment confirmed","data":{}})

#         except:
#             raise
            

