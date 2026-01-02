from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    
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
    

    path("SellerOreder/",SellerOreder.as_view()),

   
    
]