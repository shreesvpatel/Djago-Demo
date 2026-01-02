from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
            
    #================== CartOrWishlist =====================#
    
    path("CartOrWishlistAdd/",CartOrWishlistAdd.as_view()),
    path("CartOrWishlistUpdate/",CartOrWishlistUpdate.as_view()),
    path("CartOrWishlistGet/",CartOrWishlistGet.as_view()),
    path("CartOrWishlistDelete/",CartOrWishlistDelete.as_view()), 
    
]