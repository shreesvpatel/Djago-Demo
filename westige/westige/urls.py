from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    # path("payment/",include("payment.urls")),
    path("product/",include("westige.product.urls")),
    path("cart/",include("westige.cart.urls")),
    path("order_payment/",include("westige.order_payment.urls")),
    
    #================== user =====================#
    
    path("register/",Registration.as_view()),
    path("Login/",Login.as_view()),
    path("Profile/",Profile.as_view()),
    path("EditProfile/",EditProfile.as_view()),
    path("ChangePassword/",ChangePassword.as_view()),
    path("ForgotPassword/",ForgotPassword.as_view()),
    path("OtpVerify/",OtpVerify.as_view()),
    path("PasswordReset/",PasswordReset.as_view()),
    path("LogOut/",LogOut.as_view()),
    
    #================== product =====================#
    
    path("ProductAdd/",ProductAdd.as_view()),
    path("ProductUpdate/",ProductUpdate.as_view()),
    path("ProductGet/",ProductGet.as_view()),
    path("ProductDelete/",ProductDelete.as_view()),
    path("ProductFilterUser/",ProductFilterUser.as_view()),
    path("OrderDateFilter/",OrderDateFilter.as_view()),
    
    
    #================== category =====================#
    
    path("CategoryAdd/",CategoryAdd.as_view()),
    path("CategoryGet/",CategoryGet.as_view()),
    path("CategoryUpdate/",CategoryUpdate.as_view()),
    path("CategoryDelete/",CategoryDelete.as_view()),
            
    #================== CartOrWishlist =====================#
    
    path("CartOrWishlistAdd/",CartOrWishlistAdd.as_view()),
    path("CartOrWishlistUpdate/",CartOrWishlistUpdate.as_view()),
    path("CartOrWishlistGet/",CartOrWishlistGet.as_view()),
    path("CartOrWishlistDelete/",CartOrWishlistDelete.as_view()),
    
    #================== Address =====================#
    path("ConfirmAddress/",ConfirmAddress.as_view()),
    path("UpdateAddress/",UpdateAddress.as_view()),
    path("GetConfirmAddress/",GetConfirmAddress.as_view()),
    path("GetConfirmAddress/",GetConfirmAddress.as_view()),
    
    #================== Order  =====================#
    # path("Orderitem/",Orderitem.as_view()),
    # path("PlaceOrder/",PlaceOrder.as_view()),
    # path("VerifyRazorpayPayment/",VerifyRazorpayPayment.as_view()),
    path("CreatePaymentLinkAPIView/",CreatePaymentLinkAPIView.as_view()),
    path("WebHookApi/",WebHookApi.as_view()),
    path("RefundApi/",RefundApi.as_view()),
    
    

    #================== OrderConfirmStep  =====================#
    
    # path("sellerconfirmorder/",OrderConfirmStep.as_view()),
    # path("orderstatusshipping/",OrderConfirmStep.as_view()),
    # path("orderdeliver/",OrderConfirmStep.as_view()),
    
    #================== Review  =====================#
    
    # path("ReviewAdd/",ReviewAdd.as_view()),
    
    
    #================== payment  =====================#
    # path("PaymentApi/",PaymentApi.as_view()),
    
    #================== payment  =====================#
    path("Get_all_Seller/",Get_all_Seller.as_view()),
    path("SellerOreder/",SellerOreder.as_view()),

   
    
]