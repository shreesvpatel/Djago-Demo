from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [

    #================== product =====================#
    
    path("ProductAdd/",ProductAdd.as_view()),
    path("ProductUpdate/",ProductUpdate.as_view()),
    path("ProductGet/",ProductGet.as_view()),
    path("ProductDelete/",ProductDelete.as_view()),
    path("ProductFilterUser/",ProductFilterUser.as_view()),
    
    
    
    #================== category =====================#
    
    path("CategoryAdd/",CategoryAdd.as_view()),
    path("CategoryGet/",CategoryGet.as_view()),
    path("CategoryUpdate/",CategoryUpdate.as_view()),
    path("CategoryDelete/",CategoryDelete.as_view()),
            
  
    
]